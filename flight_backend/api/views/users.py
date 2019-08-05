from rest_framework.response import Response
from rest_framework import generics
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from api.models import get_user, User
from api.helpers import validate_email, validate_password, validate_login_details
from api.permissions import IsOwner
from api.serializers import (
    UserSerializer,
    TokenSerializer,
    UserLoginSerializer,
    ImageUploadSerializer,
)


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSignUpViewSet(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = validate_email(request.data.get("email"))
        password = validate_password(request.data.get("password"))
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        if email and password and first_name and last_name:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                token_serializer = TokenSerializer(
                    data={
                        "token": jwt_encode_handler(
                            jwt_payload_handler(get_user(serializer.data.get("id")))
                        )
                    }
                )
                if token_serializer.is_valid():
                    response = {
                        "token": token_serializer.data.get("token"),
                        "id": serializer.data.get("id"),
                        "first_name": serializer.data.get("first_name"),
                        "last_name": serializer.data.get("last_name"),
                        "email": serializer.data.get("email"),
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            dict(message="email, password, firstname and lastname are required"),
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLoginViewSet(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        authenticated_user = validate_login_details(request.data)
        if authenticated_user:
            serializer = UserLoginSerializer(authenticated_user)
            token_serializer = TokenSerializer(
                data={
                    "token": jwt_encode_handler(
                        jwt_payload_handler(get_user(serializer.data.get("id")))
                    )
                }
            )
            if token_serializer.is_valid():
                response = serializer.data
                response.update({"token": token_serializer.data.get("token")})
                return Response(response, status=status.HTTP_200_OK)
        return Response(
            dict(message="Login not successful, check email and password."),
            status=status.HTTP_401_UNAUTHORIZED,
        )


class UpdateUserViewSet(APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    def put(self, request, pk):
        user = get_object_or_404(User.objects.all(), pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                dict(
                    message="{} has been updated successfully".format(
                        serializer.data.get("first_name")
                    )
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            dict(message="User not updated"), status=status.HTTP_400_BAD_REQUEST
        )


class PhotoUploadViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.profile_photo:
            serializer = ImageUploadSerializer(user)
            return Response(
                data={
                    "message": "Successful",
                    "photo URL": serializer.data.get("profile_photo"),
                },
                status=status.HTTP_200_OK,
            )
        else:
            raise ValidationError("User does not have a Photo")

    def post(self, request):
        photo = request.FILES.get("image", None)
        if photo:
            user = request.user
            photo.name = "user_{}_{}".format(user.id, photo.name)
            user.profile_photo = photo
            user.save()
            serializer = ImageUploadSerializer(user)
            return Response(
                data={
                    "message": "Successful Upload",
                    "photo URL": serializer.data.get("profile_photo"),
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            raise ValidationError("Photo not supplied")

    def delete(self, request):
        user = request.user
        if user.profile_photo:
            user.profile_photo.delete(save=True)
            return Response(
                data={"message": "Photo deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            data={"message": "User does not have a Photo"}, status=status.HTTP_200_OK
        )
