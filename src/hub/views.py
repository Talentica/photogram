#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-01 09:36

"""
views.py
"""

from rest_framework import viewsets, status
from hub.models import Photo, Shared
from hub.serializers import PhotoSerializer
from photogram.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from hub.utils import encode, decode
import datetime
from jwt.exceptions import ExpiredSignatureError


__author__ = "Toran Sahu  <toran.sahu@yahoo.com>"
__license__ = "Distributed under terms of the MIT license."


class PhotoViewSet(viewsets.ModelViewSet):
    """Photo View Sets"""

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        global permission_classes

        if self.request.user.is_superuser or self.request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(
                self.queryset.filter(owner=self.request.user)
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        url_path="^shared/(?P<shared_id>[a-zA-Z0-9-]+)",
        url_name="get-shared",
        permission_classes=[],
    )
    def get_shared(self, request, shared_id):
        """Get shared image"""

        token = None
        result = Shared.objects.filter(id=shared_id).values()
        if len(result) == 0:
            return Response({"detail": "Invalid URL"}, status.HTTP_400_BAD_REQUEST)
        elif len(result) > 1:
            return Response(
                {"detail": "Duplicate entry found"}, status.HTTP_400_BAD_REQUEST
            )

        token = result[0]["token"]

        # handle jwt.exceptions.ExpiredSignatureError; if token expired
        try:
            payload = decode(token)
            photo_id = payload["id"]
        except ExpiredSignatureError:
            return Response(
                {"detail": "Link has been expired"}, status.HTTP_400_BAD_REQUEST
            )
        if photo_id is None:
            return Response({"detail": "Invalid URL"}, status.HTTP_400_BAD_REQUEST)
        photo = Photo.objects.filter(id=photo_id)
        # if photo.id is None:
        # return Response({"detail": "Data has been removed"}, status.HTTP_204)

        page = self.paginate_queryset(photo)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(photo, many=True)
        return Response(serializer.data)

    @action(
        methods=["POST"],
        detail=False,
        url_path="^share/(?P<photo_id>[0-9]+)",
        url_name="share-it",
    )
    def share_it(self, request, photo_id):

        # TODO: Handle expired token exception

        # token = encode(
        # {"id": photo_id, "exp": datetime.utcnow() + datetime.timedelta(hours=72)}
        # )
        token = encode({"id": photo_id})
        # token = "f82f5464a38a713b5e8484725064716b3035dd47"
        shared_item = Shared.objects.create(photo_id=photo_id, token=token)
        shared_item.save()
        url = f"http://127.0.0.1:8000/v1/photo/shared/{shared_item.id}/"
        content = {"sharable_url": url}
        return Response(content, status=status.HTTP_201_CREATED)
