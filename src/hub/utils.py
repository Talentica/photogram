#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2018-11-02 20:33

"""
utils.py
"""


import jwt


__author__ = "Toran Sahu  <toran.sahu@yahoo.com>"
__license__ = "Distributed under terms of the MIT license."


SECRET = "ToPsEcReT"
ALGORITHM = "HS256"


def encode(payload):
    """Encode to JWT"""
    binary_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return binary_token.decode()


def decode(token):
    """Decode JWT"""
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
