from django.db import models
from api.common.models import BaseModel, UUIDBaseModel

class OrderStatusEnum(models.TextChoices):
    NEW = 'new'
    PROCESSING = 'processing'
    COMPLETED = 'completed'

# Order Model
# UUID field is used to identify the customer who placed the order
# Loosely coupled with the identity service 
class Order(UUIDBaseModel):
    customer = models.UUIDField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='new', choices=OrderStatusEnum.choices)
    
    def __str__(self):
        return 'Order: ' + str(self.id) + ' - ' + str(self.total)

# Order Item Model
# UUID field is used to identify the product
# Loosely coupled with the catalog service
class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.UUIDField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return 'Order item for product ' + str(self.product) + ' - ' + str(self.quantity)