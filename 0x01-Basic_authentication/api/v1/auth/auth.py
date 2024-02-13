#!/usr/bin/env python3
""" class authentication to be used here """
from flask import request
from typing import List, TypeVar


class Auth:
    """ authentication class here"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth
            Args:
                path: path to file
                excluded_paths: path not inlcuded
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ authentication header function """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user function """
        return None
