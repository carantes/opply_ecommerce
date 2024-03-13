from django.urls import path, include
from rest_framework import routers

from api.catalog.views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.root_view_name = 'catalog_root'

# Set the title for the API
router.APIRootView.__name__ = 'Catalog Root'

urlpatterns = [
    # Products
    path('', include(router.urls)),
]
