#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-01 09:32

"""
serializers.py
"""

from rest_framework import serializers 
from hub.models import Photo
from django.contrib.auth.models import User


__author__ = 'Toran Sahu  <toran.sahu@yahoo.com>'


class PhotoSerializer(serializers.ModelSerializer):
    """Photo Serializer Class"""
#     owner = serializers.HiddenField(
#        default=serializers.CurrentUserDefault()
#     )
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
              default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Photo
        fields = "__all__"
        read_only_fields = ('uploaded_at', 'updated_at')
