from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.orders.models import Order
from api.orders.serializers import OrderSerializer

# Order viewset
class OrderViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows orders to be viewed or edited.
    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)