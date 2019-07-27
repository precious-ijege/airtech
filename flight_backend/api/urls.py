from django.urls import path

from .views import UserSignUpViewSet, UserLoginViewSet, UpdateUserViewSet

urlpatterns = [
    path("sign-up/", UserSignUpViewSet.as_view(), name="sign-up"),
    path("log-in/", UserLoginViewSet.as_view(), name="log-in"),
    path("update-profile/<int:pk>", UpdateUserViewSet.as_view(), name="update-profile"),
]
