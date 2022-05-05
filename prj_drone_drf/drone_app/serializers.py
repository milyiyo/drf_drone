from rest_framework import serializers

from prj_drone_drf.drone_app.models import Drone, Medication


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
