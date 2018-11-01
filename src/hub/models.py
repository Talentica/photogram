#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-10-31 15:38

"""
models.py
"""

from django.db import models
from django.contrib.auth.models import User


__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


class Photo(models.Model):
    """Photo Collection Model"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    image = models.ImageField()
    title = models.CharField(max_length=256)
    uploaded_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-uploaded_at', )

    def __str__(self):
        return str(self.title)
