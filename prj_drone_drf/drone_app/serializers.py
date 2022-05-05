from rest_framework import serializers

from prj_drone_drf.drone_app.models import Drone, Medication
from prj_drone_drf.drone_app.utils import validate_fleet_size


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drone
        fields = [
            'id',
            'serial_number',
            'model',
            'weight_limit',
            'battery_capacity',
            'state',
            'medications'
        ]

    def validate(self, data):
        validate_fleet_size(Drone, serializers.ValidationError)
        return data


class MedicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medication
        fields = [
            'id',
            'image',
            'weight',
            'name',
            'code'
        ]
