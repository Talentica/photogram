#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-05 15:44

"""
dev_settings.py
"""

from photogram.base_settings import *

__author__ = "Toran Sahu <toran.sahu@yahoo.com>"
__license__ = "Distributed under terms of the MIT license"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "photogram",
        # "USER": "root",
        "USER": "dev",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
