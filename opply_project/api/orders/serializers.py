from rest_framework import serializers

from api.orders.models import Order, OrderItem, OrderStatusEnum
from api.catalog.services import InventoryManagementService

# Order Item Serializer
class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


    
# Order Serializer
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_items', 'total', 'status', 'url', 'public_id']

    # Validate
        # Order item quantity should be greater than 0
        # Order total should be greater than 0
        # Order status should be 'new' or 'completed'
    def validate(self, attrs):
        if attrs['total'] <= 0:
            raise serializers.ValidationError("Total should be greater than 0")
        for order_item in attrs['order_items']:
            if order_item['quantity'] <= 0:
                raise serializers.ValidationError("Order item quantity should be greater than 0")
        
        if attrs.get('status') == '' or attrs.get('status') == None:
            attrs['status'] = OrderStatusEnum.NEW

        if attrs['status'] not in [OrderStatusEnum.NEW, OrderStatusEnum.COMPLETED]:
            raise serializers.ValidationError("Status should be 'new' or 'completed'")    
        
        return attrs
         
    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items')

        order_items = (instance.order_items).all()
        order_items = list(order_items)
        instance.total = validated_data.get('total', instance.total)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        for order_item_data in order_items_data:
            order_item = order_items.pop(0)
            order_item.product = order_item_data.get('product', order_item.product)
            order_item.quantity = order_item_data.get('quantity', order_item.quantity)
            order_item.price = order_item_data.get('price', order_item.price)
            order_item.save()
        return instance

    def create(self, validated_data):
        if validated_data['status'] == OrderStatusEnum.NEW:
            for order_item in validated_data['order_items']:
                InventoryManagementService().update_inventory(order_item['product'], order_item['quantity'])
            
            # If all items are available, set the order status to 'completed'
            validated_data['status'] = OrderStatusEnum.COMPLETED

        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item in order_items_data:
            OrderItem.objects.create(order=order, **order_item)
        return order