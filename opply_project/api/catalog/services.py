from api.catalog.models import Product

# Custom Exception
class InventoryManagementException(Exception):
    pass

# Inventory Management Service facade
class InventoryManagementService:
    def update_inventory(self, product_uuid, quantity):
        product = Product.get_product_by_public_id(product_uuid)
            
        if product is None:
            raise InventoryManagementException('Product not found')
        
        # Ship the product from the inventory
        if product.inventory.ship(quantity) == False:
            raise InventoryManagementException('Requested quantity is not available.')
        
        product.save()


    def get_available_inventory(self, product_uuid):
        product = Product.get_product_by_public_id(product_uuid)

        if product is None:
            raise InventoryManagementException('Product not found')

        return product.inventory.available
        
