from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from api import models
from .forms import UserAdminCreationForm, UserAdminChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    search_fields = ("email", "first_name", "last_name")
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_superuser",
        "updated_at",
    )
    fieldsets = (
        ("Details", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "is_staff",
                    "is_superuser",
                    "password",
                    "password2",
                ),
            },
        ),
    )

    ordering = ("email", "first_name", "last_name")


# Register your models here.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Aircraft)
admin.site.register(models.Location)
admin.site.register(models.Flight)
admin.site.register(models.Ticket)

# Remove Group Model from Admin.
admin.site.unregister(Group)
