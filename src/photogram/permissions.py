#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-10-31 15:13

"""
permissions.py
"""

from rest_framework.permissions import BasePermission


__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsUser(BasePermission):
    """Owner and admin only will have all permissions."""
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj == request.user

        return False


class IsAuthenticatedOrReadOnly(BasePermission):
    """The request is authenticated as a user, or is a read-only requ  est.
    """
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS
                and request.query_params.get('token')):
            # TODO: check for valid token
            if(True):
                return True
            return False
        if (request.user and request.user.is_superuser):
            return True
        return False 
