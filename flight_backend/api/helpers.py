import re

from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate

from .constants import PASSWORD_MESSAGE, PASSWORD_REGEX, EMAIL_REGEX, EMAIL_MESSAGE

from .models import User, Location, Aircraft


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
    email = login_details.get('email')
    password = login_details.get('password')
    if email and password:
        user = authenticate(email=email, password=password)
        return user
    raise exceptions.ValidationError(
        "You must enter an email and a password to login"
    )
