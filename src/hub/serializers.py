#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-01 09:32

"""
serializers.py
"""

from rest_framework.serializers import ModelSerializer
from hub.models import Photo


__author__ = 'Toran Sahu  <toran.sahu@yahoo.com>'


class PhotoSerializer(ModelSerializer):
    """Photo Serializer Class"""

    class Meta:
        model = Photo
        fields = '__all__'


