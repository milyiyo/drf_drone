from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json


class DroneAPITests(APITestCase):
    url = '/api/v1/drones/'

    def setUp(self):
        ...

    def test_empty_fleet(self):
        # WHEN
        response = self.client.get(self.url, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(0, response_data['count'])

    def test_drone_creation(self):
        # GIVEN
        data = {
            'serial_number': 'drone_01',
            'model': 'Lightweight',
            'weight_limit': 100,
            'battery_capacity': 100
        }
        # WHEN
        response = self.client.post(self.url, data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check the response data
        response_data = json.loads(response.content)
        self.assertEqual(data['serial_number'], response_data['serial_number'])
        self.assertEqual(data['model'], response_data['model'])
        self.assertEqual(float(data['weight_limit']),
                         float(response_data['weight_limit']))
        self.assertEqual(int(data['battery_capacity']), int(
            response_data['battery_capacity']))

    def test_drone_update(self):
        # GIVEN
        data = {
            'serial_number': 'drone_01',
            'model': 'Lightweight',
            'weight_limit': 100,
            'battery_capacity': 100
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        drone_id = response_data['id']

        # WHEN
        response = self.client.patch(
            path=f'{self.url}{drone_id}/',
            data={'weight_limit': 50},
            format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        drone_weight_limit = response_data['weight_limit']
        self.assertEqual(drone_weight_limit, '50.00')

    def test_fleet_limit(self):
        ...

    def test_error_carrying_medications(self):
        ...

    def test_battery_below_25(self):
        ...

    def test_serial_number_length(self):
        ...

    def test_weight_below_limit(self):
        ...

    def test_weight_above_limit(self):
        ...

    def test_load_with_medications(self):
        ...

    def test_exceeded_capacity_limit(self):
        ...
