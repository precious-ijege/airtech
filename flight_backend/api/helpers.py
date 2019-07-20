import re
from rest_framework import serializers
from .constants import PASSWORD_MESSAGE, PASSWORD_REGEX, EMAIL_REGEX, EMAIL_MESSAGE

from .models import User


def validate_password(password):
    """
    Validate password
    """
    if re.search(PASSWORD_REGEX, password) is not None:
        return password
    raise serializers.ValidationError(PASSWORD_MESSAGE)


def validate_email(email):
    """
    Validate email and username
    """
    if re.search(EMAIL_REGEX, email) is None:
        raise serializers.ValidationError(EMAIL_MESSAGE)
    elif User.objects.filter(email=email).exists():
        raise serializers.ValidationError("Email already exist")
    else:
        return email
