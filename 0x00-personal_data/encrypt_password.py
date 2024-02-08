#!/usr/bin/env python3
""" encrypt password """
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash password function """
    password = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)
