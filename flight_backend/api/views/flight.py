from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.models import Aircraft, Location, Flight, Ticket
from api.serializers import LocationSerializer, AircraftSerializer, FlightSerializer


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)


class AircraftViewSet(ModelViewSet):
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)


class FlightViewSet(ModelViewSet):

    """
    POST flight/
    GET flight/
    GET flight/:pk/
    PUT flight/:pk/
    DELETE flight/:pk/
    """

    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = FlightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
