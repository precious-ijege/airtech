from rest_framework import serializers

from api import models

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "created_at",
            "updated_at",
            "last_login",
        )

        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "last_login": {"read_only": True},
        }

    def get_full_name(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)
