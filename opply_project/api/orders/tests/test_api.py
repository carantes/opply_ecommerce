from django.urls import reverse
from rest_framework import status
from api.common.tests import APITestSetup

from api.catalog.services import InventoryManagementService

class OrderTests(APITestSetup):
    fixtures = ['Users.json', 'Products.json', 'Inventory.json', 'Orders.json', 'Order-Items.json']

    def test_get_orders(self):
        """
        Ensure we can get a list of orders.
        """
        url = reverse('order-list')
        response = self.client.get(url)
        
        # Ensure we have a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 2 orders are loaded from the fixture
        self.assertEqual(len(response.data.get('results')), 2)
        self.assertEqual(response.data.get('count'), 2)

        # # Ensure we have the correct data
        results = response.data.get('results')    
        self.assertEqual(results[0].get('customer'), '9feeac87-9058-4c97-a347-ee0b356ee8a0')
        self.assertEqual(results[0].get('total'), '2000.00')
        self.assertEqual(results[0].get('status'), 'completed')
    
    def test_get_order(self):
        """
        Ensure we can get an order.
        """
        url = reverse('order-detail', args=[1])
        response = self.client.get(url)
        
        # Ensure we have a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure we have the correct data
        self.assertEqual(response.data.get('customer'), '9feeac87-9058-4c97-a347-ee0b356ee8a0')
        self.assertEqual(response.data.get('total'), '2000.00')
        self.assertEqual(response.data.get('status'), 'completed')

    def test_create_order_without_update_inventory(self):
        """
        Ensure we can create a new order without updating the inventory.
        """
        url = reverse('order-list')
        data = {'customer': '9feeac87-9058-4c97-a347-ee0b356ee8a0', 'total': 3000, 'order_items': [{'product': 'd8d4d3f5-1a9e-4b0d-9d5e-2d5d3d9e0b1e', 'quantity': 3, 'price': 1000}], 'status': 'completed' }
        response = self.client.post(url, data, format='json')
        
        # Ensure we have a successful response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('customer'), '9feeac87-9058-4c97-a347-ee0b356ee8a0')
        self.assertEqual(response.data.get('total'), '3000.00')
        self.assertEqual(response.data.get('order_items')[0].get('product'), 'd8d4d3f5-1a9e-4b0d-9d5e-2d5d3d9e0b1e')
        self.assertEqual(response.data.get('status'), 'completed')
    
    def test_create_order_with_update_inventory(self):
        """
        Ensure we can create a new order and update the inventory.
        """
        url = reverse('order-list')
        data = {'customer': '9feeac87-9058-4c97-a347-ee0b356ee8a0', 'total': 3000, 'order_items': [{'product': '04d5d8be-470b-45e8-b3fe-88b1c412535a', 'quantity': 3, 'price': 1000}] }
        
        # Ensure we have the correct inventory before the order
        self.assertEqual(InventoryManagementService.get_available_inventory(self, '04d5d8be-470b-45e8-b3fe-88b1c412535a'), 52)
        
        response = self.client.post(url, data, format='json')
        
        # Ensure we have a successful response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('customer'), '9feeac87-9058-4c97-a347-ee0b356ee8a0')
        self.assertEqual(response.data.get('total'), '3000.00')
        self.assertEqual(response.data.get('order_items')[0].get('product'), '04d5d8be-470b-45e8-b3fe-88b1c412535a')
        self.assertEqual(response.data.get('status'), 'completed')

        # Ensure we have the correct inventory after the order
        self.assertEqual(InventoryManagementService.get_available_inventory(self, '04d5d8be-470b-45e8-b3fe-88b1c412535a'), 49)
    