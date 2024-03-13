from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.identity.models import Customer

# Register your models here.
admin.site.register(Customer, UserAdmin)