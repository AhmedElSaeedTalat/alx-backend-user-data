#!/usr/bin/env python3
""" encrypt password """
import bcrypt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    """ hash password function """
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)
