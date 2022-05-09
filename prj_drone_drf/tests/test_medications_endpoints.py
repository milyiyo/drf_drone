from rest_framework import status
from rest_framework.test import APITestCase
import json


class MedicationAPITests(APITestCase):
    medication_url = '/api/v1/medications/'

    def test_error_creating_with_wrong_name(self):
        # GIVEN
        medication_data = {
            'name': '*******',
            'code': 'COD_01',
            'weight': 100,
        }
        # WHEN
        response = self.client.post(
            self.medication_url, medication_data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = json.loads(response.content)
        error_text = resp_data['name'][0]
        self.assertEqual(
            error_text, 'Allowed only letters, numbers, ‘-‘, ‘_’.')

    def test_error_creating_with_wrong_code(self):
        # GIVEN
        medication_data = {
            'name': 'med_01',
            'code': 'code',
            'weight': 100,
        }
        # WHEN
        response = self.client.post(
            self.medication_url, medication_data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = json.loads(response.content)
        error_text = resp_data['code'][0]
        self.assertEqual(
            error_text, 'Allowed only upper case letters, underscore and numbers.')

    def test_weight_below_limit(self):
        # GIVEN
        medication_data = {
            'name': 'med_01',
            'code': 'COD_01',
            'weight': -1,
        }
        # WHEN
        response = self.client.post(
            self.medication_url, medication_data, format='json')
        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = json.loads(response.content)
        error_text = resp_data['weight'][0]
        self.assertEqual(
            error_text, 'Ensure this value is greater than or equal to 1.')
