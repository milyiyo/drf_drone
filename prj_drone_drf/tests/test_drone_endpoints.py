import json

from rest_framework import status
from rest_framework.test import APITestCase


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

    def test_error_carrying_medications_single_item(self):
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

    def test_error_carrying_medications_multiple_items(self):
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
            'weight': 10
        }
        response = self.client.post(
            self.medication_url, med_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        med_data = json.loads(response.content)

        # Try to load the drone with a weight higher than its limit.
        drone_medications_url = f"{self.drone_url}{drone_data['id']}/medications/"
        response = self.client.put(drone_medications_url, [
                                   med_data['id']]*20, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        resp_data = json.loads(response.content)
        self.assertEqual(
            resp_data['detail'], "The list of medications cannot be loaded because exceed the drone\'s capacity")

    def test_successful_load_of_medications(self):
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
        for i in range(2):
            med_data = {
                'name': f'med_{i}',
                'code': f'COD_{i}',
                'weight': 50
            }
            response = self.client.post(
                self.medication_url, med_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Load two medications successfully
        drone_medications_url = f"{self.drone_url}{drone_data['id']}/medications/"
        response = self.client.put(
            drone_medications_url, [1, 2], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_load_of_repeated_medications(self):
        # GIVEN
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

        # Create the medications
        for i in range(2):
            med_data = {
                'name': f'med_{i}',
                'code': f'COD_{i}',
                'weight': 20
            }
            response = self.client.post(
                self.medication_url, med_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # WHEN
        # Load multiples medications of the same type.
        #   med_01 -> 2 items
        #   med_02 -> 3 items
        drone_medications_url = f"{self.drone_url}{drone_data['id']}/medications/"
        response = self.client.put(
            drone_medications_url, [1, 1, 2, 2, 2], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # THEN
        response = self.client.get(self.drone_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        load_info = response_data['results'][0]['load_info']
        quantity_info = {x['medication']: x['quantity'] for x in load_info}
        # Check the following amounts
        #   med_01 -> 2 items
        #   med_02 -> 3 items
        self.assertEqual(quantity_info[1], 2)
        self.assertEqual(quantity_info[2], 3)

    def test_battery_below_25(self):
        # GIVEN
        # Create the drone
        drone_data = {
            'serial_number': 'drone_01',
            'model': 'Lightweight',
            'weight_limit': 100,
            'battery_capacity': 10
        }
        response = self.client.post(self.drone_url, drone_data, format='json')
        resp_data = json.loads(response.content)
        # WHEN
        # Update the state to LOADING
        response = self.client.patch(
            path=f"{self.drone_url}{resp_data['id']}/",
            data={'state': 'LOADING'},
            format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = json.loads(response.content)
        self.assertEqual(
            resp_data[0], 'The drone cannot be in LOADING state if its battery level is below 25%')

    def test_serial_number_length(self):
        # GIVEN
        drone_data = {
            'serial_number': 'a'*101,
            'model': 'Lightweight',
            'weight_limit': 100,
            'battery_capacity': 10
        }
        # WHEN
        response = self.client.post(self.drone_url, drone_data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = json.loads(response.content)
        error_text = resp_data['serial_number'][0]
        self.assertEqual(
            error_text, 'Ensure this field has no more than 100 characters.')

    def test_weight_below_limit(self):
        # GIVEN
        drone_data = {
            'serial_number': 'drone_01',
            'model': 'Lightweight',
            'weight_limit': -10,
            'battery_capacity': 10
        }
        # WHEN
        response = self.client.post(self.drone_url, drone_data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = json.loads(response.content)
        error_text = resp_data['weight_limit'][0]
        self.assertEqual(
            error_text, 'Ensure this value is greater than or equal to 1.')

    def test_weight_above_limit(self):
        # GIVEN
        drone_data = {
            'serial_number': 'drone_01',
            'model': 'Lightweight',
            'weight_limit': 600,
            'battery_capacity': 10
        }
        # WHEN
        response = self.client.post(self.drone_url, drone_data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = json.loads(response.content)
        error_text = resp_data['weight_limit'][0]
        self.assertEqual(
            error_text, 'Ensure this value is less than or equal to 500.')

    def test_error_creating_drone_wrong_state(self):
        # GIVEN
        drone_data = {
            'serial_number': 'drone_01',
            'model': 'Lightweight',
            'weight_limit': 100,
            'battery_capacity': 10,
            'state': 'INVALID_STATE'
        }
        # WHEN
        response = self.client.post(self.drone_url, drone_data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = json.loads(response.content)
        error_text = resp_data['state'][0]
        self.assertEqual(
            error_text, '"INVALID_STATE" is not a valid choice.')

    def test_error_creating_drone_wrong_model(self):
        # GIVEN
        drone_data = {
            'serial_number': 'drone_01',
            'model': 'INVALID_MODEL',
            'weight_limit': 100,
            'battery_capacity': 10,
        }
        # WHEN
        response = self.client.post(self.drone_url, drone_data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = json.loads(response.content)
        error_text = resp_data['model'][0]
        self.assertEqual(
            error_text, '"INVALID_MODEL" is not a valid choice.')
