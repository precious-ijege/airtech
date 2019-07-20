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
            "password",
            "email",
            "phone_number",
            "contact_address",
            "created_at",
            "updated_at",
            "last_login",
        )

        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "last_login": {"read_only": True},
        }

    def get_full_name(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)

    def create(self, validated_data):
        password = validated_data.get("password")
        user = models.User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """

    token = serializers.CharField(max_length=255)
