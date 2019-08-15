from rest_framework import serializers

from api import models


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = (
            "id",
            "country",
            "country_code",
            "city",
        )


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Aircraft
        fields = (
            "id",
            "name",
            "model",
        )


class FlightSerializer(serializers.ModelSerializer):
    departure = LocationSerializer()
    destination = LocationSerializer()
    aircraft = AircraftSerializer()

    class Meta:
        model = models.Flight
        fields = (
            "id",
            "flight_number",
            "departure_date",
            "arrival_date",
            "flight_duration",
            "economy_price_currency",
            "economy_price",
            "business_price_currency",
            "business_price",
            "status",
            "created_at",
            "updated_at",
            "departure",
            "destination",
            "aircraft",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
        depth = 1

    def create(self, validated_data):
        import pdb; pdb.set_trace()
        departure = models.Location.objects.get(id=validated_data.pop("departure"))
        destination = models.Location.objects.get(
            id=validated_data.pop("destination")
        )
        aircraft = models.Aircraft.objects.get(id=validated_data.pop("aircraft"))
        flight_object = models.Flight.objects.create(
            departure=departure,
            destination=destination,
            aircraft=aircraft,
            **validated_data
        )

        return flight_object
