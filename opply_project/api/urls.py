from django.urls import path, include, path
from api.identity import urls as identity_urls
from api.catalog import urls as catalog_urls
from api.orders import urls as order_urls
from api.views import api_root

urlpatterns = [
    path('', api_root),
    path(r'identity/', include(identity_urls)),
    path(r'catalog/', include(catalog_urls)),
    path(r'orders/', include(order_urls)),
]