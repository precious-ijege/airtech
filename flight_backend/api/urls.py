from django.urls import path
from rest_framework.routers import SimpleRouter


from .views import UsersViewSet

router = SimpleRouter()

router.register("users", UsersViewSet, "users")
urlpatterns = []

urlpatterns += router.urls
