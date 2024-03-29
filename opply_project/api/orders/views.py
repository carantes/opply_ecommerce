from django.db import transaction
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.orders.models import Order, OrderStatusEnum
from api.orders.serializers import OrderSerializer
from api.catalog.services import InventoryManagementService, InventoryManagementException
from api.common.token import get_user_public_id_from_token

# Order viewset
class OrderViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows orders to be viewed or edited.
    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''
        Restric the returned orders to the authenticated user.
        '''
        customer = get_user_public_id_from_token(self.request)
        return Order.objects.filter(customer=customer)

    def create(self, request):
        '''
        API endpoint that allows a new order to be created.
        '''
        serializer = OrderSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Create the order and update the inventory in a transaction
            with transaction.atomic():
                # Set the customer to the order
                customer = get_user_public_id_from_token(request)
                order = serializer.save(customer=customer)

                # Only update the inventory if the order is new
                if order.status == OrderStatusEnum.NEW:
                    inventoryService = InventoryManagementService()
                    try:
                        for order_item in order.order_items.all():
                            inventoryService.update_inventory(order_item.product, order_item.quantity)
                        
                        order.status = OrderStatusEnum.COMPLETED
                        order.save()

                    # Rollback the transaction if there is an error on the inventory update
                    except InventoryManagementException as e:
                        # Need to explicitly set the rollback to True
                        transaction.set_rollback(True)
                        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)