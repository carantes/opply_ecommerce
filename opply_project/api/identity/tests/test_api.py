from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from api.identity.models import Customer
from api.common.tests import APITestSetup

# Register User
class RegisterUserTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register_user')
        username = 'opplynewuser'
        data = {'username': username, 'email': 'newuser@opply.com', 'password': 'opply123', 'password2': 'opply123'}
        
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Customer.objects.count(), 1)

# User Authentication
class UserAuthenticationTests(APITestCase):
    fixtures = ['Users.json', 'Customers.json']

    def test_user_login(self):
        """
        Ensure we can login a user.
        """
        url = reverse('token_obtain_pair')
        data = {'username': 'opply_test', 'password': 'test@1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

# Customer Viewset
class CustomerTests(APITestSetup):
    fixtures = ['Users.json', 'Customers.json']

    def test_get_customers(self):
        """
        Ensure we can get a list of customers.
        """

        url = reverse('customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results')
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].get('username'), 'opply')
        self.assertEqual(results[1].get('public_id'), '9feeac87-9058-4c97-a347-ee0b356ee8a1')

    def test_create_customer(self):
        """
        Ensure we can create a new customer.
        """
        url = reverse('customer-list')
        data = {'username': 'newcustomer', 'email': 'newcustomer@opply.com', 'password': 'opply123', 'password2': 'opply123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('username'), 'newcustomer')
    
    def test_update_customer(self):
        """
        Ensure we can update an existing customer.
        """
        url = reverse('customer-detail', args=[1])
        data = {'username': 'updatedcustomer', 'email': 'updatedcustomer@opply.com', 'password': 'opply123', 'password2': 'opply123'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('username'), 'updatedcustomer')
    
    def test_delete_customer(self):
        """
        Ensure we can delete an existing customer.
        """
        url = reverse('customer-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
    
    def test_get_customer(self):
        """
        Ensure we can get a single customer.
        """
        url = reverse('customer-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('username'), 'opply')
        self.assertEqual(response.data.get('public_id'), '9feeac87-9058-4c97-a347-ee0b356ee8a0')