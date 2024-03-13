from django.contrib import admin
from api.catalog.models import Product, Inventory

admin.site.register(Product)
admin.site.register(Inventory)