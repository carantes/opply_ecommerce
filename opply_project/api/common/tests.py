from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from api.identity.models import Customer
class APITestSetup(APITestCase):
    
    def setUp(self):
        # Get user
        self.user = User.objects.get(username='opply_test')

        # Set the user credentials
        refresh_token = RefreshToken.for_user(self.user)

        # # Set user claims
        refresh_token['email'] = self.user.email
        refresh_token['public_id'] = '9feeac87-9058-4c97-a347-ee0b356ee8a1'

        print('refresh_token', refresh_token)
        print('access_token', refresh_token.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh_token.access_token)}')
