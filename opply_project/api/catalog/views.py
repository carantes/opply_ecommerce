from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.catalog.models import Product, Inventory
from api.catalog.serializers import ProductSerializer, InventoryShipSerializer

# Product viewset
class ProductViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows products to be viewed or edited.
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    # Extra actions to update the inventory
    @action(detail=True, methods=['post'], serializer_class=InventoryShipSerializer)
    def ship(self, request, pk=None):
        '''
        API endpoint that allows a product item to be shipped from the inventory.
        '''
        serializer = InventoryShipSerializer(data=request.data)

        if serializer.is_valid():
            serializer.update(Inventory.objects.get(Product_id=pk), serializer.validated_data)
            
            # TODO: return the new inventory status
            return Response({'status': 'Product was shipped'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
