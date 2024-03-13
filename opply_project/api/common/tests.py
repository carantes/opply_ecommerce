from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

class APITestSetup(APITestCase):
    
    def setUp(self):
        # Get user
        self.user = User.objects.get(username='opply_test')

        # Set the user credentials
        refresh_token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh_token.access_token)}')
