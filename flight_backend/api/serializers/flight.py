from rest_framework import serializers

from api import models
from api.serializers import UserSerializer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = "__all__"


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Aircraft
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flight
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["departure"] = LocationSerializer(instance.departure).data
        response["destination"] = LocationSerializer(instance.destination).data
        response["aircraft"] = AircraftSerializer(instance.aircraft).data

        return response


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = UserSerializer(instance.user).data
        response["flight"] = FlightSerializer(instance.flight).data

        return response
