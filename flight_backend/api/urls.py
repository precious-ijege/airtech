from django.urls import path

from .views import UserSignUpViewSet

urlpatterns = [path("sign-up/", UserSignUpViewSet.as_view(), name="sign-up")]
