#!/usr/bin/env python3
""" encrypt password """
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash password function """
    password = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check if is valid """
    password = password.encode()
    return bcrypt.checkpw(password, hashed_password)
