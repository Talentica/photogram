#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-01 12:19

"""
tests.py
"""

from rest_framework.test import APITestCase
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import status
from PIL import Image
from tempfile import NamedTemporaryFile


__author__ = "Toran Sahu <toran.sahu@yahoo.com>"
__license__ = "Distributed under terms of the MIT license"


# Create your tests here.


class PhotoAnonymousTests(APITestCase):
    """Tests hub app that:

    Anonymous user can:
        - not POST Photos
        - not PUT Photos
        - not PATCH Photos
        - not DELETE Photos
        - not GET(s) Photos without shareable token
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
