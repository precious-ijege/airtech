import uuid
from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.translation import ugettext_lazy as _
from .. import constants


class Aircraft(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    capacity = models.PositiveSmallIntegerField(default=500)

    def __str__(self):
        return f"{self.manufacturer} {self.model}"


class Location(models.Model):
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=4)
    city = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.city}, {self.country}"


class Flight(models.Model):
    """
    This model defines a Flight object
    """

    flight_number = models.CharField(
        _("Enter flight number"), max_length=50, blank=True, unique=True
    )
    departure_date = models.DateField(_("Departure Date"), blank=True, null=True)
    arrival_date = models.DateField(_("Arrival Date"), blank=True, null=True)
    departure = models.ForeignKey(
        "Location", on_delete=models.SET_NULL, null=True, related_name="departure"
    )
    destination = models.ForeignKey(
        "Location", on_delete=models.SET_NULL, null=True, related_name="destination"
    )
    flight_duration = models.DurationField(blank=True)
    economy_price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", null=True, blank=True
    )
    business_price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", null=True, blank=True
    )
    aircraft = models.ForeignKey("Aircraft", on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=50, choices=constants.FLIGHT_STATUS, default=constants.AVAILABLE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.flight_number)


class Ticket(models.Model):
    """
    Model defines a Ticket object
    """

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=50, blank=True)
    ticket_class = models.CharField(max_length=10, choices=constants.CLASS)
    passport_number = models.CharField(max_length=50)
    status = models.CharField(
        choices=constants.STATUS, max_length=50, blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if len(self.ticket_id.strip(" ")) == 0:
            self.ticket_id = self.id_generator()
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.ticket_id)

    def id_generator(self):
        return uuid.uuid4().hex.upper()[0:9]
