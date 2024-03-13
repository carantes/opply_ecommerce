from django.urls import path, include
from rest_framework import routers

from api.orders.views import OrderViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.root_view_name = 'orders_root'

# Set the title for the API
router.APIRootView.__name__ = 'Orders Root'


urlpatterns = [
    # Products
    path('', include(router.urls)),
]
