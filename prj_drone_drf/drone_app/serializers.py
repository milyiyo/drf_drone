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

    def update(self, instance, validated_data):
        # Prevent the drone from being loaded with more weight that it can carry
        sum_weight_medications = sum(
            [m.weight for m in validated_data['medications']])
        if validated_data['weight_limit'] < sum_weight_medications:
            raise serializers.ValidationError(
                "The sum of medications' weight can't exceed the drone's capacity")

        # Prevent the drone from being in LOADING state if the battery level is **below 25%**
        if validated_data['battery_capacity'] < 25 and validated_data['state'] == 'LOADING':
            raise serializers.ValidationError(
                "The drone cannot be in LOADING state if its battery level is below 25%")

        super().update(instance, validated_data)
        return instance


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
