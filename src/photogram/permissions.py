#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-10-31 15:13

"""
permissions.py
"""

from rest_framework.permissions import BasePermission


__author__ = "Toran Sahu <toran.sahu@yahoo.com>"
__license__ = "Distributed under terms of the MIT license"


SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]


class IsAuthenticatedOrReadOnly(BasePermission):
    """The request is authenticated as a user, or is a read-only requ  est.
    """

    message = "[warn] - Unauthorized Access"

    def has_permission(self, request, view):
        if (
            (request.user and request.user.is_authenticated)
            or request.user.is_superuser
            or request.user.is_staff
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser or request.user.is_staff:
                return True
            if request.user.is_anonymous:
                return False
            else:
                try:
                    return obj.owner == request.user
                except:
                    return False
        return False
