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
from rest_framework.response import Response


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

    def list(self, request, *args, **kwargs):
        global permission_classes

        if self.request.user.is_superuser or self.request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(self.queryset.filter(owner=self.request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
