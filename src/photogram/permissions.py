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

