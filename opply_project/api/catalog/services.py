from api.catalog.models import Product
from rest_framework import serializers

class InventoryManagementService():
    def update_inventory(self, product_uuid, quantity):
        product = Product.get_product_by_public_id(product_uuid)
            
        if product is None:
            raise serializers.ValidationError('Product not found.')
        
        if product.inventory.reserve(quantity) == False:
            raise serializers.ValidationError('Requested quantity is not available.')
        
        product.save()


    def get_available_inventory(self, product_uuid):
        product = Product.get_product_by_public_id(product_uuid)
        return product.inventory.available
        
