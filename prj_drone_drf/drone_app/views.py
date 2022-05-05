from rest_framework import viewsets
from prj_drone_drf.drone_app.models import Drone, Medication

from prj_drone_drf.drone_app.serializers import DroneSerializer, MedicationSerializer


class DroneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows drones to be viewed or edited.
    """
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer


class MedicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows medications to be viewed or edited.
    """
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
