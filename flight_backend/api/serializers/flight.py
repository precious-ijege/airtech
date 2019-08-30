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

    def create(self, validated_data):
        flight_object = models.Flight.objects.create(**validated_data)

        return flight_object

    def update(self, instance, validated_data):
        instance.flight_number = validated_data.get(
            "flight_number", instance.flight_number
        )
        instance.departure_date = validated_data.get(
            "departure_date", instance.departure_date
        )
        instance.arrival_date = validated_data.get(
            "arrival_date", instance.arrival_date
        )
        instance.flight_duration = validated_data.get(
            "flight_duration", instance.flight_duration
        )
        instance.economy_price_currency = validated_data.get(
            "economy_price_currency", instance.economy_price_currency
        )
        instance.economy_price = validated_data.get(
            "economy_price", instance.economy_price
        )
        instance.business_price_currency = validated_data.get(
            "business_price_currency", instance.business_price_currency
        )
        instance.business_price = validated_data.get(
            "business_price", instance.business_price
        )
        instance.status = validated_data.get("status", instance.status)
        instance.departure = validated_data.get("departure", instance.departure)
        instance.destination = validated_data.get("destination", instance.destination)
        instance.aircraft = validated_data.get("aircraft", instance.aircraft)

        instance.save()
        return instance


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

    def create(self, validated_data):
        ticket = models.Ticket.objects.create(**validated_data)

        return ticket
