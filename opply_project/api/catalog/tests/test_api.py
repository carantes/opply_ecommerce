from django.urls import reverse
from rest_framework import status
from api.common.tests import APITestSetup
from api.catalog.models import Product

class ProductTests(APITestSetup):
    fixtures = ['Users.json', 'Products.json']

    def test_get_products(self):
        """
        Ensure we can get a list of products.
        """
        url = reverse('product-list')
        response = self.client.get(url)
        
        # Ensure we have a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 20 products are loaded from the fixture, return 10 per page
        self.assertEqual(len(response.data.get('results')), 10)
        self.assertEqual(response.data.get('count'), 20)

        # Ensure we have the correct data
        results = response.data.get('results')    
        self.assertEqual(results[0].get('name'), 'Django Reinhardt')
        self.assertEqual(results[0].get('description'), 'Gypsy jazz guitar')
        self.assertEqual(results[0].get('price'), '100.00')

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        url = reverse('product-list')
        data = {'name': 'New Product', 'description': 'New Product description', 'price': 300}
        response = self.client.post(url, data, format='json')
        
        # Ensure we have a successful response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), 'New Product')
        self.assertEqual(response.data.get('description'), 'New Product description')
        self.assertEqual(response.data.get('price'), '300.00')
    
    def test_update_product(self):
        """
        Ensure we can update an existing product.
        """
        url = reverse('product-detail', args=[1])
        data = {'name': 'Django Reinhardt', 'description': 'Gypsy jazz guitar updated', 'price': 100.0 }
        response = self.client.put(url, data, format='json')
        
        # Ensure we have a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('description'), 'Gypsy jazz guitar updated')
        self.assertEqual(response.data.get('price'), '100.00')
    
    def test_delete_product(self):
        """
        Ensure we can delete an existing product.
        """
        
        # Ensure we have a product to delete
        self.assertEqual(Product.objects.count(), 20)
        
        url = reverse('product-detail', args=[1])
        response = self.client.delete(url)
        
        # Ensure we have a successful response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 19)
    
    def test_get_product(self):
        """
        Ensure we can get a single product.
        """
        url = reverse('product-detail', args=[1])
        response = self.client.get(url)
        
        # Ensure we have a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure we have the correct data
        self.assertEqual(response.data.get('name'), 'Django Reinhardt')
        self.assertEqual(response.data.get('description'), 'Gypsy jazz guitar')
        self.assertEqual(response.data.get('price'), '100.00')
    
    