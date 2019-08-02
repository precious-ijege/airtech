import json
import tempfile
from shutil import rmtree

from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework.views import status
from django.conf import settings
from PIL import Image

from api.models import User

client = APIClient()


def generate_random_image():
    image = Image.new("RGB", (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file)
    return tmp_file


class ImageUploadTest(APITestCase):
    settings.MEDIA_ROOT += "test"

    def setUp(self):
        self.url = reverse("photo")
        self.user = User.objects.create_user(
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

    def tearDown(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_authenticated_user_cant_upload_without_photo(self):
        response = client.post(
            self.url, HTTP_AUTHORIZATION="Token {}".format(self.token)
        )
        self.assertEqual(response.data[0], "Photo not supplied")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_without_photo_cant_retrieve_photo(self):
        response = client.get(
            self.url, HTTP_AUTHORIZATION="Token {}".format(self.token)
        )
        self.assertEqual(response.data[0], "User does not have a Photo")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_without_photo_cant_delete_photo(self):
        response = client.delete(
            self.url, HTTP_AUTHORIZATION="Token {}".format(self.token)
        )
        self.assertEqual(response.data["message"], "User does not have a Photo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_upload_photo(self):
        tmp_file = generate_random_image()
        response = client.post(
            self.url,
            data={"image": tmp_file},
            HTTP_AUTHORIZATION="Token {}".format(self.token),
        )
        self.assertEqual(response.data["message"], "Successful Upload")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_can_get_photo(self):
        tmp_file = generate_random_image()
        client.post(
            self.url,
            data={"image": tmp_file},
            HTTP_AUTHORIZATION="Token {}".format(self.token),
        )
        response = client.get(
            self.url, HTTP_AUTHORIZATION="Token {}".format(self.token)
        )
        self.assertEqual(response.data["message"], "Successful")
        self.assertIn("photo URL", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_delete_photo(self):
        tmp_file = generate_random_image()
        client.post(
            self.url,
            data={"image": tmp_file},
            HTTP_AUTHORIZATION="Token {}".format(self.token),
        )
        response = client.delete(
            self.url, HTTP_AUTHORIZATION="Token {}".format(self.token)
        )
        self.assertEqual(response.data["message"], "Photo deleted successfully")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
