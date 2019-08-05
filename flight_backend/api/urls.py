from django.urls import path

from .views import (
    UserSignUpViewSet,
    UserLoginViewSet,
    UpdateUserViewSet,
    PhotoUploadViewSet,
)

urlpatterns = [
    path("users/sign-up/", UserSignUpViewSet.as_view(), name="sign-up"),
    path("users/log-in/", UserLoginViewSet.as_view(), name="log-in"),
    path(
        "users/update-profile/<int:pk>",
        UpdateUserViewSet.as_view(),
        name="update-profile",
    ),
    path("users/photo", PhotoUploadViewSet.as_view(), name="photo"),
]
