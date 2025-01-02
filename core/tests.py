# app_name/tests/test_design.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Design  # Replace 'app_name' with your actual app name


class DesignTests(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')  # Log the user in

    def test_create_design(self):
        # URL to create a new design
        url = '/api/designs/'  # Make sure this matches your URL pattern for creating designs
        data = {
            'name': 'Test Design',
            'version': 1,  # Use integer value for version
            'dimensions': {'width': 10, 'height': 10, 'depth': 10},  # Correct format for dimensions
            'material_specs': {'type': 'Cardboard', 'color': 'Brown'}  # Correct format for material_specs
        }

        # Send POST request to create the design
        response = self.client.post(url, data, format='json')

        # Assert that the design was successfully created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the design was saved in the database
        self.assertEqual(Design.objects.count(), 1)
        design = Design.objects.first()
        self.assertEqual(design.name, 'Test Design')
        self.assertEqual(design.version, 1)
        self.assertEqual(design.dimensions, {'width': 10, 'height': 10, 'depth': 10})
        self.assertEqual(design.material_specs, {'type': 'Cardboard', 'color': 'Brown'})

    def test_create_design_unauthenticated(self):
        # Log out the user to simulate an unauthenticated request
        self.client.logout()

        url = '/api/designs/'
        data = {
            'name': 'Test Design',
            'version': 1,
            'dimensions': {'width': 10, 'height': 10, 'depth': 10},
            'material_specs': {'type': 'Cardboard', 'color': 'Brown'}
        }

        # Attempt to create a design while logged out
        response = self.client.post(url, data, format='json')

        # Assert that the unauthenticated request is denied (401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_design(self):
        # Send invalid data (e.g., missing required fields or incorrect formats)
        url = '/api/designs/'
        data = {
            'name': '',  # Invalid: Name cannot be empty
            'version': '',  # Invalid: Version cannot be empty
            'dimensions': 'invalid',  # Invalid: Invalid format for dimensions
            'material_specs': ''  # Invalid: Material specs cannot be empty
        }

        response = self.client.post(url, data, format='json')

        # Assert that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if specific validation errors are returned
        self.assertIn('name', response.data)
        self.assertIn('version', response.data)
        self.assertIn('dimensions', response.data)
        self.assertIn('material_specs', response.data)

    def test_get_designs(self):
        Design.objects.create(
            name='Test Design 1',
            version=1,
            dimensions={'width': 10, 'height': 10, 'depth': 10},
            material_specs={'type': 'Cardboard', 'color': 'Brown'}
        )

        url = '/api/designs/'
        response = self.client.get(url)

        # Assert that the response is successful and contains the design
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # We have one design in the database
        self.assertEqual(response.data[0]['name'], 'Test Design 1')

    def test_update_design(self):
        design = Design.objects.create(
            name='Test Design 1',
            version=1,
            dimensions={'width': 10, 'height': 10, 'depth': 10},
            material_specs={'type': 'Cardboard', 'color': 'Brown'}
        )

        url = f'/api/designs/{design.id}/'
        updated_data = {
            'name': 'Updated Design',
            'version': 2,  # Updated version as integer
            'dimensions': {'width': 15, 'height': 15, 'depth': 15},  # Updated dimensions
            'material_specs': {'type': 'Plastic', 'color': 'Blue'}  # Updated material_specs
        }

        response = self.client.put(url, updated_data, format='json')

        # Assert that the design was updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Design')
        self.assertEqual(response.data['version'], 2)
        self.assertEqual(response.data['dimensions'], {'width': 15, 'height': 15, 'depth': 15})
        self.assertEqual(response.data['material_specs'], {'type': 'Plastic', 'color': 'Blue'})

    def test_delete_design(self):
        design = Design.objects.create(
            name='Test Design 1',
            version=1,
            dimensions={'width': 10, 'height': 10, 'depth': 10},
            material_specs={'type': 'Cardboard', 'color': 'Brown'}
        )

        url = f'/api/designs/{design.id}/'
        response = self.client.delete(url)

        # Assert that the design was deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Design.objects.count(), 0)  # Ensure the design was deleted
