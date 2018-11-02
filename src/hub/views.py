#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-01 09:36

"""
views.py
"""

from rest_framework import viewsets
from hub.models import Photo
from hub.serializers import PhotoSerializer
from photogram.permissions import IsUser, IsAuthenticatedOrReadOnly


__author__ = 'Toran Sahu  <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license.'


class PhotoViewSet(viewsets.ModelViewSet):
    """Photo View Sets"""

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    # TODO: fix to not pass anonymous user to serializer
    permission_classes = (
            # IsUser &
            IsAuthenticatedOrReadOnly,
    )
