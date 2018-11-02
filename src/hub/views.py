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


__author__ = "Toran Sahu  <toran.sahu@yahoo.com>"
__license__ = "Distributed under terms of the MIT license."


class PhotoViewSet(viewsets.ModelViewSet):
    """Photo View Sets"""

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    # TODO: fix to not pass anonymous user to serializer
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
        url_path="^token/(?P<token>[a-zA-Z0-9]+)",
        url_name="get-shared",
        permission_classes=[],
    )
    def get_shared(self, request, token):
        """Get shared image"""
        payload = decode(token)
        photo_id = payload["id"]
        if photo_id is None:
            return Response({"detail": "Invalid URL"}, status.HTTP_400_BAD_REQUEST)
        # TODO: check expiration of token
        created_at = payload["created_at"]
        expires_in = payload["expires_in"]

        photo = Photo.objects.filter(id=photo_id)
        if photo.id is None:
            return Response({"detail": "Data has been removed"}, status.HTTP_204)

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
        token = encode({"id": photo_id, "created_at": None, "expires_in": None})
        # token = "f82f5464a38a713b5e8484725064716b3035dd47"
        shared_item = Shared.objects.create(photo_id=photo_id, token=token)
        shared_item.save()
        url = f"http://127.0.0.1:8000/v1/photo/token/{token}/"
        content = {"sharable_url": url}
        return Response(content, status=status.HTTP_201_CREATED)
