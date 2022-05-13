from django.http.response import Http404
from prj_drone_drf.drone_app.models.drone import Drone
from prj_drone_drf.drone_app.models.load_information import LoadInformation
from prj_drone_drf.drone_app.models.medication import Medication
from prj_drone_drf.drone_app.serializers import (DroneSerializer,
                                                 MedicationSerializer)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class DroneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows drones to be viewed or edited.
    """
    allowed_methods = ['post', 'patch', 'get', 'put']
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer

    # The service should allow:
    # [x] registering a drone;
    # [x] loading a drone with medication items;
    # [x] checking loaded medication items for a given drone;
    # [x] checking available drones for loading;
    # [x] check drone battery level for a given drone;

    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request, *args, **kwargs):
        """
        Get the available drones. 
        - Available drones are those in state IDLE and with more than 25% of battery. 
        """
        filtered = Drone.objects.filter(
            battery_capacity__gt=25, state__exact='IDLE')
        serializer = self.get_serializer(filtered, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='battery')
    def battery(self, request, *args, **kwargs):
        drone = self.get_object()
        if not drone:
            raise Http404
        serializer = self.get_serializer(drone)
        response_data = {
            'battery_capacity': f"{serializer.data['battery_capacity']}%"
        }
        return Response(response_data)

    @action(detail=True, methods=['get', 'put'])
    def medications(self, request, *args, **kwargs):
        drone: Drone = self.get_object()
        if not drone:
            raise Http404

        if request.method == 'GET':
            load_info = LoadInformation.objects.filter(drone__pk=drone.pk)
            serializer = MedicationSerializer(
                [x.medication for x in load_info], many=True)
            quantities = [x.quantity for x in load_info]
            res = [{'quantity': x[0], 'medication':x[1]}
                   for x in zip(quantities, serializer.data)]
            return Response(res)

        if request.method == 'PUT':
            med_ids = request.data
            medications = Medication.objects.filter(pk__in=med_ids)

            # Verify that all medications id are present
            if len(set(med_ids)) != medications.count():
                stored_ids = [m.pk for m in medications]
                not_found_ids = [id for id in med_ids if id not in stored_ids]
                return Response(data={
                    'detail': f'From the medication ids provided the following were not found: {not_found_ids}'
                }, status=404)

            # Check the drone's weight limit
            weight_medications = sum(
                [sum([med.weight for med in medications if med.pk == _id]) for _id in med_ids])
            if drone.weight_limit < weight_medications:
                return Response(data={
                    'detail': "The list of medications cannot be loaded because exceed the drone's capacity"
                }, status=406)

            # Remove previous rows of LoadInformation related to the drone
            drone_rows = LoadInformation.objects.filter(drone__pk=drone.pk)
            drone_rows.delete()
            # Create the new relations in LoadInformation
            for m in medications:
                load_inst = LoadInformation(drone=drone,
                                            medication=m,
                                            quantity=len([x for x in med_ids if x == m.pk]))
                load_inst.save()

            serializer = self.get_serializer(drone)
            return Response(serializer.data)


class MedicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows medications to be viewed or edited.
    """
    allowed_methods = ['post', 'get']
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
