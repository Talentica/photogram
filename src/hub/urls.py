#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-01 09:41

"""
urls.py
"""


from rest_framework.routers import DefaultRouter
from hub.views import PhotoViewSet


__author__ = 'Toran Sahu  <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license.'


app_name = "hub"

router = DefaultRouter()
router.register('', PhotoViewSet)

urlpatterns = router.urls
