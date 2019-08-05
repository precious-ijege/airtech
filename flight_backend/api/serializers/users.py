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

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.contact_address = validated_data.get(
            "contact_address", instance.contact_address
        )
        if validated_data.get("password"):
            instance.set_password(validated_data.get("password"))

        instance.save()
        return instance


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """

    token = serializers.CharField(max_length=255)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id", "first_name", "last_name", "email")


class ImageUploadSerializer(serializers.ModelSerializer):
    """
    Handles file/image upload by a user
    """

    class Meta:
        model = models.User
        fields = ("id", "profile_photo")
