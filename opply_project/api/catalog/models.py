from django.db import models
from api.common.models import UUIDBaseModel, BaseModel

class Product(UUIDBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name + ' (' + str(self.public_id) + ')'
    
    def get_product_by_public_id(public_id):
        return Product.objects.get(public_id=public_id)


class Inventory(BaseModel):
    Product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    available = models.IntegerField()
    shipped = models.IntegerField(default=0)
 
    # Ships the product from the inventory
    def ship(self, quantity):
        if self.available >= quantity:
            self.available -= quantity
            self.shipped += quantity
            self.save()
            return True
        
        return False

    def __str__(self):
        return f'Inventory for {self.Product.name}, {self.available} available, {self.shipped} shipped'
