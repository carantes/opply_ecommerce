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
    reserved = models.IntegerField(default=0)
    shipped = models.IntegerField(default=0)

    # Reserves the product if it is in stock
    def reserve(self, quantity):
        if self.available >= quantity:
            self.available -= quantity
            self.reserved += quantity
            self.save()
            return True
        return False
    
    # Ships the product if it is reserved or in stock
    def ship(self, quantity):
        if self.reserved >= quantity:
            self.reserved -= quantity
            self.shipped += quantity
            self.save()
            return True
        elif (self.reserved + self.available) >= quantity:
            # Fall back to using available stock
            self.available -= quantity-self.reserved
            self.reserved = 0
            self.shipped += quantity            
            self.save()
            return True
        
        return False

    def __str__(self):
        return f'Inventory for {self.Product.name}, {self.available} available, {self.reserved} reserved, {self.shipped} shipped'
