from django.urls import path, include
from rest_framework import routers

from api.orders.views import OrderViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    # Products
    path('', include(router.urls)),
]
