import re

from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate

from .constants import (
    PASSWORD_MESSAGE,
    PASSWORD_REGEX,
    EMAIL_REGEX,
    EMAIL_MESSAGE,
    STATUSES,
)

from .models import User


def validate_password(password):
    """
    Validate password
    """
    if re.search(PASSWORD_REGEX, password) is not None:
        return password
    raise exceptions.ValidationError(PASSWORD_MESSAGE)


def validate_email(email):
    """
    Validate email and username
    """
    if re.search(EMAIL_REGEX, email) is None:
        raise serializers.ValidationError(EMAIL_MESSAGE)
    elif User.objects.filter(email=email).exists():
        raise exceptions.ValidationError("Email already exist")
    else:
        return email


def validate_login_details(login_details):
    email = login_details.get("email")
    password = login_details.get("password")
    if email and password:
        user = authenticate(email=email, password=password)
        return user
    raise exceptions.ValidationError("You must enter an email and a password to login")


def validate_flight_details(flight_details):
    if not flight_details.get("flight_number"):
        raise exceptions.ValidationError("Flight must have a flight number")
    elif flight_details.get("departure_date") > flight_details.get("arrival_date"):
        raise exceptions.ValidationError("Departure date cannot be after Arrival date")
    elif not (
        flight_details.get("economy_price") and flight_details.get("business_price")
    ):
        raise exceptions.ValidationError(
            "Please include both economy and business Prices"
        )
    elif flight_details.get("status") not in STATUSES:
        raise exceptions.ValidationError(
            "Flight status must be either AVAILABLE, DEPARTED, DELAYED, CANCELLED, LANDED, or ARRIVED"
        )
    elif flight_details.get("economy_price_currency") != flight_details.get(
        "business_price_currency"
    ):
        raise exceptions.ValidationError(
            "Currency type for business and economy price must be the same"
        )
    elif not (
        flight_details.get("destination")
        and flight_details.get("departure")
        and flight_details.get("aircraft")
    ):
        raise exceptions.ValidationError(
            "Provide valid keys for destination, departure and aircraft"
        )
    else:
        return flight_details
