#!/usr/bin/env python3
""" BasicAuth to be used here """
from .auth import Auth
import re


class BasicAuth(Auth):
    """ BasicAuth class here"""
    def extract_base64_authorization_header(self, authorization_header: str) \
            -> str:
        """ base64 encoding """
        if not authorization_header:
            return None
        elif type(authorization_header) is not str:
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        pattern = r'(?<=Basic ).+'
        match = re.findall(pattern, authorization_header)
        return match[0]
