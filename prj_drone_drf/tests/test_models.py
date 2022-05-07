from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json


class DroneAPITests(APITestCase):
    drone_url = '/api/v1/drones/'
    medication_url = '/api/v1/medications/'

    def setUp(self):
        ...

    def test_empty_fleet(self):
        # WHEN
        response = self.client.get(self.drone_url, format='json')
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
        response = self.client.post(self.drone_url, data, format='json')
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
        response = self.client.post(self.drone_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        drone_id = response_data['id']

        # WHEN
        response = self.client.patch(
            path=f'{self.drone_url}{drone_id}/',
            data={'weight_limit': 50},
            format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        drone_weight_limit = response_data['weight_limit']
        self.assertEqual(drone_weight_limit, '50.00')

    def test_fleet_limit(self):
        FLEET_LIMIT = 10
        data_template = {
            'serial_number': '',
            'model': 'Lightweight',
            'weight_limit': 100,
            'battery_capacity': 100
        }
        for i in range(FLEET_LIMIT):
            data_template['serial_number'] = f'drone_{i}'
            resp_iter = self.client.post(
                self.drone_url, data_template, format='json')
            # Check the first 10th are created
            self.assertEqual(resp_iter.status_code, status.HTTP_201_CREATED)

        # Check the error at the 11th.
        resp_iter = self.client.post(
            self.drone_url, data_template, format='json')
        self.assertEqual(resp_iter.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the count is equal to the limit
        response = self.client.get(self.drone_url, format='json')
        response_data = json.loads(response.content)
        self.assertEqual(FLEET_LIMIT, response_data['count'])

    def test_error_carrying_medications(self):
        # Create the drone
        drone_data = {
            'serial_number': 'drone_01',
            'model': 'Lightweight',
            'weight_limit': 100,
            'battery_capacity': 100
        }
        response = self.client.post(self.drone_url, drone_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        drone_data = json.loads(response.content)

        # Create the medication
        med_data = {
            'name': 'med_01',
            'code': 'COD_01',
            'weight': 200
        }
        response = self.client.post(
            self.medication_url, med_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        med_data = json.loads(response.content)

        # Try to load the drone with a weight higher than its limit.
        drone_medications_url = f"{self.drone_url}{drone_data['id']}/medications/"
        response = self.client.put(drone_medications_url, [
                                   med_data['id']], format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

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
