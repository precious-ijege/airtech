from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from api.models import Aircraft, Location, Flight, Ticket
from api.serializers import (
    LocationSerializer,
    AircraftSerializer,
    FlightSerializer,
    TicketSerializer,
)
from api.helpers import validate_flight_details
from api.constants import STATUSES, AVAILABLE, BOOKED
from api.tasks import flight_booking_notification, flight_reservation_notification


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)


class AircraftViewSet(ModelViewSet):
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)


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

    def get_permissions(self):
        """
        Set and get permissions for the flight view.
        """

        if self.action == "status":
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAuthenticated, IsAdminUser)

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        validate_flight_details(request.data)
        serializer = FlightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super(FlightViewSet, self).update(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def status(self, request):
        flight_status = request.query_params.get("status").upper()
        if flight_status not in STATUSES:
            return Response(
                dict(
                    message="Sorry, {} is Invalid. Status can be either AVAILABLE, DEPARTED, DELAYED, CANCELLED, LANDED, ARRIVED".format(
                        flight_status
                    )
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        flight = Flight.objects.filter(status=flight_status)
        if len(flight) > 0:
            return Response(
                dict(
                    message="{} Flights".format(flight_status),
                    data=FlightSerializer(flight, many=True).data,
                ),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                dict(message="Sorry, we have no flight in this category at the moment"),
                status=status.HTTP_200_OK,
            )


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["post"]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        flight = get_object_or_404(Flight.objects.all(), pk=request.data.get("flight"))
        if flight.status != AVAILABLE:
            return Response(
                dict(message="You cant book/reserve an unavailable flight."),
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get("status") == BOOKED:
            # payment module goes in here
            self.perform_create(serializer)
            flight_booking_notification.delay(serializer.data.get("id"))
            return Response(
                dict(message="Ticket has been booked", data=serializer.data),
                status=status.HTTP_200_OK,
            )
        else:
            # payment module goes in here
            self.perform_create(serializer)
            flight_reservation_notification.delay(serializer.data.get("id"))
            return Response(
                dict(
                    message="Your Ticket has been Reserved, Make full payment in the next 24hrs to avoid ticket forfeit",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )

    @action(detail=False, methods=["post"])
    def reserved(self, request):
        ticket = get_object_or_404(
            Ticket.objects.all(), ticket_id=request.data.get("ticket_id")
        )
        if ticket.user.email != request.user.email:
            return Response(
                dict(message="Ticket does not belong to you"),
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if (ticket.user.email == request.user.email) and ticket.status != BOOKED:
            # payment module goes in here
            ticket.status = BOOKED
            ticket.save()
            ticket.refresh_from_db()
            serializer = TicketSerializer(ticket)
            flight_booking_notification.delay(serializer.data.get("id"))
            return Response(
                dict(message="Ticket has been booked", data=serializer.data),
                status=status.HTTP_200_OK,
            )
        else:
            serializer = TicketSerializer(ticket)
            return Response(
                dict(message="You already paid for this Ticket", data=serializer.data),
                status=status.HTTP_200_OK,
            )
