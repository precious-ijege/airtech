from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from ..constants import (
    EMAIL_REGEX,
    EMAIL_MESSAGE,
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, **kwargs):
        email = kwargs.pop("email")
        password = kwargs.get("password")
        if not email:
            raise ValueError("Email address is required")
        if not password:
            raise ValueError("Password address is required")
        user_obj = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)

        return user_obj

    def create_user(self, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)

        return self._create_user(**kwargs)

    def create_superuser(self, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(**kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(max_length=50,
                              unique=True,
                              validators=[
                                  RegexValidator(
                                      regex=EMAIL_REGEX,
                                      message=EMAIL_MESSAGE,
                                      code='invalid_email'
                                  )
                              ])
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    objects = UserManager()

    def get_fullname(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return self.email
