from rest_framework import serializers

from api.catalog.models import Product, Inventory

# Product serializer
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    quantity = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='available',
        source='inventory',
        default=0,
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'url', 'public_id']
        read_only_fields = ['public_id']

    
# Inventory Ship serializer
class InventoryShipSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(write_only=True, required=True, min_value=1)
    
    class Meta:
        model = Inventory
        fields = ['product', 'available', 'shipped']
    
    def update(self, inventory, validated_data):
        if not inventory.ship(validated_data['quantity']):
            raise serializers.ValidationError('Requested quantity is not available.')
        
        return inventory
        