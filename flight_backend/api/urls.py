from django.urls import path
from rest_framework.routers import SimpleRouter


from .views import (
    UserSignUpViewSet,
    UserLoginViewSet,
    UpdateUserViewSet,
    PhotoUploadViewSet,
    LocationViewSet,
    AircraftViewSet,
    FlightViewSet,
    TicketViewSet,
    index,
)

router = SimpleRouter()

router.register("location", LocationViewSet, "location")
router.register("aircraft", AircraftViewSet, "aircraft")
router.register("flight", FlightViewSet, "flight")
router.register("ticket", TicketViewSet, "ticket")

urlpatterns = [
    path("", index, name="home"),
    path("users/sign-up/", UserSignUpViewSet.as_view(), name="sign-up"),
    path("users/log-in/", UserLoginViewSet.as_view(), name="log-in"),
    path(
        "users/update-profile/<int:pk>",
        UpdateUserViewSet.as_view(),
        name="update-profile",
    ),
    path("users/photo", PhotoUploadViewSet.as_view(), name="photo"),
]

urlpatterns += router.urls
