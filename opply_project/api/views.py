from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'identity': reverse('identity_root', request=request, format=format),
        'catalog': reverse('catalog_root', request=request, format=format),
        'orders': 'TODO: Add the orders API here.'
    })