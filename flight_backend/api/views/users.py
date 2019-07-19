from rest_framework.response import Response
from rest_framework import generics
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.models import get_user
from ..helpers import validate_email, validate_password
from api.serializers import UserSerializer, TokenSerializer


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