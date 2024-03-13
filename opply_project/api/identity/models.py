from django.db import models
from django.contrib.auth.models import User
import uuid

class Customer(User):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.username + ' (' + str(self.public_id) + ')'
    
    def get_customer_by_public_id(public_id):
        return Customer.objects.get(public_id=public_id)
