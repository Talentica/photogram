#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-01 15:26

"""
settings.py
"""


import socket


__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


if socket.gethostname() in ('ToranS-UB', 'mint-ThinkPad-L440', ):
    from photogram.base_settings import *
