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


__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


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

    def setUp(self):
        self.teardown()
        test_user = AnonymousUser()

    def tearDown(self):
        try:
            pass
        except ObjectDoesNotExist:
            pass

    def test_create_photo(self):
        # TODO: put image obj here
        data = {'image': 'put image obj here', 'title': 'Test Image'}
        response = self.client.post(reverse('hub-v1:photo-list'), data=data)
        self.assertEqual(response.stats_code, status.HTTP_401_UNAUTHORIZED)



