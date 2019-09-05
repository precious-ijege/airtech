import json

from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework.views import status

from api.models import User, Aircraft

client = APIClient()


class AircraftApiTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            first_name="Ghost",
            last_name="Ghost",
            email="ghost@gmail.com",
            password="password1*",
        )
        self.login_details = {"email": "ghost@gmail.com", "password": "password1*"}
        self.response = client.post(
            reverse("log-in"),
            data=json.dumps(self.login_details),
            content_type="application/json",
        )
        self.token = self.response.data["token"]
        self.aircraft_new = Aircraft.objects.create(
            id=2, name="Boeing", manufacturer="Boeing Jets", model="757", capacity=500
        )
        self.aircraft_count_before = Aircraft.objects.count()

    def test_admin_can_create_an_aircraft_object(self):
        new_aircraft = {
            "name": "Airbus",
            "manufacturer": "Airbus Corperate",
            "model": "A380",
            "capacity": 320,
        }
        response = client.post(
            reverse("aircraft-list"),
            data=json.dumps(new_aircraft),
            HTTP_AUTHORIZATION="Token {}".format(self.token),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Aircraft.objects.count(), self.aircraft_count_before + 1)
        self.assertIn("manufacturer", response.data)

    def test_admin_can_get_all_aircraft_objects(self):
        response = client.get(
            reverse("aircraft-list"), HTTP_AUTHORIZATION="Token {}".format(self.token)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Aircraft.objects.count(), self.aircraft_count_before)

    def test_admin_can_get_an_aircraft_object(self):
        url = reverse("aircraft-detail", args=(self.aircraft_new.id,))
        response = client.get(url, HTTP_AUTHORIZATION="Token {}".format(self.token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.aircraft_new.name)

    def test_admin_can_delete_an_aircraft_object(self):
        url = reverse("aircraft-detail", args=(self.aircraft_new.id,))
        response = client.delete(url, HTTP_AUTHORIZATION="Token {}".format(self.token))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_update_a_location_object(self):
        url = reverse("aircraft-detail", args=(self.aircraft_new.id,))
        new_model = {"model": "BB10"}
        response = client.patch(
            url,
            data=json.dumps(new_model),
            HTTP_AUTHORIZATION="Token {}".format(self.token),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("model"), new_model.get("model"))
