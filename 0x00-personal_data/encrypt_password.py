#!/usr/bin/env python3
""" encrypt password """
import bcrypt


def hash_password(password: str) -> str:
    """ hash password function """
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)
