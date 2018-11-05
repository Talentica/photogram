#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-01 12:19

"""
tests.py
"""

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import status
from PIL import Image
from tempfile import NamedTemporaryFile
from hub.views import PhotoViewSet
from django.test.client import encode_multipart
from hub.models import Photo


__author__ = "Toran Sahu <toran.sahu@yahoo.com>"
__license__ = "Distributed under terms of the MIT license"


# Create your tests here.


class PhotoAuthUserTest(APITestCase):
    """Test Hub app that
    Authenticated User can:
        - POST Photos
        - PUT Photos
        - PATCH Photos
        - DELETE Photos
        - GET(s) Photos without shareable token
        - Generate (POST) a shareable link for a photo
    """

    def setUp(self):
        self.tearDown()
        self.test_user = User.objects.create_user(
            username="testuser", email="test@gmail.com", password="password@Test"
        )
        self.auth_token = None
        self.photo_data = None
        self.photo_id = None
        self.shared_link = None

        # create temp image for testing
        self.test_image = Image.new("RGB", (50, 50))
        self.test_file = NamedTemporaryFile(suffix=".png")
        self.test_image.save(self.test_file)

        test_photo = Photo.objects.create(
            title="test sample data",
            image="http://testserver.com/",
            owner=self.test_user,
        )
        self.photo_id = test_photo.id

    def tearDown(self):
        try:
            test_user = User.objects.get_by_natural_key("testuser")
            test_user.delete()
        except ObjectDoesNotExist:
            pass

    def test_get_auth_token(self):
        user_cred = {"username": "testuser", "password": "password@Test"}
        response = self.client.post("/v1/auth/token/create/", data=user_cred)
        self.auth_token = response.data["auth_token"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_photo_list(self):
        factory = APIRequestFactory()
        view = PhotoViewSet.as_view({"get": "list"})
        request = factory.get(reverse("hub-v1:photo-list"))
        force_authenticate(request, user=self.test_user, token=self.auth_token)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_photo(self):
        with open(self.test_file.name, "rb") as image_data:
            self.photo_data = {"image": image_data, "title": "Test Image"}
            photo_data = self.photo_data
            BOUNDARY = "BoUnDaRyStRiNg"
            content = encode_multipart(BOUNDARY, photo_data)
            content_type = f"multipart/form-data; boundary={BOUNDARY}"
            factory = APIRequestFactory()
            view = PhotoViewSet.as_view({"post": "create"})
            request = factory.post(
                reverse("hub-v1:photo-list"), content, content_type=content_type
            )
            force_authenticate(request, user=self.test_user, token=self.auth_token)
            response = view(request)
            self.photo_id = response.data["id"]
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_photo(self):
        with open(self.test_file.name, "rb") as image_data:
            self.photo_data = {"image": image_data, "title": "Test Image Updated"}
            photo_data = self.photo_data
            BOUNDARY = "BoUnDaRyStRiNg"
            content = encode_multipart(BOUNDARY, photo_data)
            content_type = f"multipart/form-data; boundary={BOUNDARY}"
            factory = APIRequestFactory()
            view = PhotoViewSet.as_view({"put": "update"})
            request = factory.put(
                reverse("hub-v1:photo-detail", kwargs={"pk": self.photo_id}),
                content,
                content_type=content_type,
            )
            force_authenticate(request, user=self.test_user, token=self.auth_token)
            response = view(request, pk=self.photo_id)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_photo(self):
        self.photo_data = {"title": "Test Image Partial Updated"}
        photo_data = self.photo_data
        BOUNDARY = "BoUnDaRyStRiNg"
        content = encode_multipart(BOUNDARY, photo_data)
        content_type = f"multipart/form-data; boundary={BOUNDARY}"
        factory = APIRequestFactory()
        view = PhotoViewSet.as_view({"patch": "partial_update"})
        request = factory.patch(
            reverse("hub-v1:photo-detail", kwargs={"pk": self.photo_id}),
            content,
            content_type=content_type,
        )
        force_authenticate(request, user=self.test_user, token=self.auth_token)
        response = view(request, pk=self.photo_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_share_it(self):
        data = {"photo_id": self.photo_id}
        factory = APIRequestFactory()
        view = PhotoViewSet.as_view({"post": "share_it"})
        request = factory.post(reverse("hub-v1:photo-share_it"), data)
        force_authenticate(request, user=self.test_user, token=self.auth_token)
        response = view(request)
        self.shared_link = response.data["sharable_url"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_shared(self):
        response = self.client.get("http://{self.shared_link}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_photo(self):
        factory = APIRequestFactory()
        view = PhotoViewSet.as_view({"delete": "destroy"})
        request = factory.delete(
            reverse("hub-v1:photo-detail", kwargs={"pk": self.photo_id})
        )
        force_authenticate(request, user=self.test_user, token=self.auth_token)
        response = view(request, pk=self.photo_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PhotoAnonymousTests(APITestCase):
    """Tests hub app that:

    Anonymous user can:
        - not POST Photos
        - not PUT Photos
        - not PATCH Photos
        - not DELETE Photos
        - not GET(s) Photos without shared link/token
        - GET Photos with shared link/token
    """

    test_file = None

    def setUp(self):
        self.tearDown()
        self.test_user = AnonymousUser()

        # create temp imgae for testing
        self.test_image = Image.new("RGB", (50, 50))
        self.test_file = NamedTemporaryFile(suffix=".png")
        # self.test_file.name = "test_image.png"
        self.test_image.save(self.test_file)

    def tearDown(self):
        try:
            # import os
            # os.remove(self.test_file.name)
            pass
        except ObjectDoesNotExist:
            pass

    def test_create_photo(self):

        # with open("test_file.jpeg", "rb") as image_data:
        # with open("test_image.png", "rb") as image_data:
        with open(self.test_file.name, "rb") as image_data:
            data = {"image": image_data, "title": "Test Image"}

            response = self.client.post(
                reverse("hub-v1:photo-list"), data=data, format="multipart"
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_photo(self):
        with open(self.test_file.name, "rb") as image_data:
            data = {"image": image_data, "title": "Test Image 2"}
            response = self.client.put(
                reverse("hub-v1:photo-detail", kwargs={"pk": 1}),
                data=data,
                format="multipart",
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_photo(self):
        data = {"title": "Test Image 3"}
        response = self.client.put(
            reverse("hub-v1:photo-detail", kwargs={"pk": 1}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_get_photo(self):
    # response = self.client.get(
    # reverse("hub-v1:photo-detail", kwargs={"pk": 1, "token": "invalid_token"})
    # )
    # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_photo(self):
        response = self.client.get(reverse("hub-v1:photo-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_photo(self):
        response = self.client.delete(reverse("hub-v1:photo-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
