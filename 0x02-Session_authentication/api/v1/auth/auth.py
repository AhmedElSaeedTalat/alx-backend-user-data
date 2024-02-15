#!/usr/bin/env python3
""" class authentication to be used here """
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ authentication class here"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth
            Args:
                path: path to file
                excluded_paths: path not inlcuded
        """
        if not path or not excluded_paths:
            return True
        modified_list = list(map(lambda i: i.strip('/'), excluded_paths))
        modified_path = path.strip('/')
        if modified_path in modified_list:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authentication header function """
        if not request:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user function """
        return None

    def session_cookie(self, request=None):
        """ session cookiee """
        if not request:
            return None
        cookie = getenv('SESSION_NAME')
        return request.cookies.get(cookie)
