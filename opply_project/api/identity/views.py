from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from api.identity.models import Customer
from api.identity.serializers import RegisterUserSerializer, CustomTokenObtainPairSerializer, CustomerSerializer

# Identity root
@api_view(['GET'])
def identity_root(request):
    return Response({
        'register': reverse('register_user', request=request),
        'token': reverse('token_obtain_pair', request=request),
        'refresh': reverse('token_refresh', request=request),
        'verify': reverse('token_verify', request=request),
        'customers': reverse('customer-list', request=request),
    })

# Register user
class RegisterUserView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

# Login user
class SignInUserView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)


# Customer Viewset (protected)
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
