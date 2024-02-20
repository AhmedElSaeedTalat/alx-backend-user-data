#!/usr/bin/env python3
""" auth file """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ function that hashes password """
    password_encoded = password.encode()
    salted = bcrypt.gensalt()
    return bcrypt.hashpw(password_encoded, salted)
