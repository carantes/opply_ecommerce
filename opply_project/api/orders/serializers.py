from rest_framework import serializers

from api.orders.models import Order, OrderItem, OrderStatusEnum

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
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item in order_items_data:
            OrderItem.objects.create(order=order, **order_item)
        return order