from unittest.case import TestCase

from django.core.exceptions import ValidationError
from prj_drone_drf.drone_app.models.drone import Drone
from prj_drone_drf.drone_app.models.load_information import LoadInformation
from prj_drone_drf.drone_app.models.medication import Medication


class LoadInformationModelTests(TestCase):

    def test_error_when_quantity_below_one(self):
        drone = Drone(weight_limit=100)
        drone.save()

        medication = Medication(weight=12)
        medication.save()

        load_info = LoadInformation(
            drone=drone, medication=medication, quantity=0)

        try:
            load_info.clean_fields()
            self.fail()
        except ValidationError as error:
            self.assertEqual(error.error_dict['quantity'][0].messages[0],
                             'Ensure this value is greater than or equal to 1.')
