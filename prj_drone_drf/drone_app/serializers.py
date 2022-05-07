from rest_framework import serializers

from prj_drone_drf.drone_app.models import Drone, Medication
from prj_drone_drf.drone_app.utils import validate_fleet_size


class DroneSerializer(serializers.ModelSerializer):
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

    medications = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all(), required=False, many=True)

    def validate(self, data):
        validate_fleet_size(Drone, serializers.ValidationError)
        return data

    def update(self, instance, validated_data):
        # Prevent the drone from being loaded with more weight that it can carry
        if 'medications' in validated_data:
            sum_weight_medications = sum(
                [m.weight for m in validated_data['medications']])
            # Get the new value if it's specified
            weight_limit = validated_data['weight_limit'] \
                if 'weight_limit' in validated_data \
                else instance.weight_limit
            if weight_limit < sum_weight_medications:
                raise serializers.ValidationError(
                    "The sum of medications' weight can't exceed the drone's capacity")

        # Prevent the drone from being in LOADING state if the battery level is **below 25%**
        battery_capacity = validated_data['battery_capacity'] \
                if 'battery_capacity' in validated_data \
                else instance.battery_capacity
        state = validated_data['state'] \
                if 'state' in validated_data \
                else instance.state
        if battery_capacity < 25 and state == 'LOADING':
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
