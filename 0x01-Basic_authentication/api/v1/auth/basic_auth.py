#!/usr/bin/env python3
""" BasicAuth to be used here """
from .auth import Auth
import re
import base64


class BasicAuth(Auth):
    """ BasicAuth class here"""
    def extract_base64_authorization_header(self, authorization_header: str) \
            -> str:
        """ base64 extract pass """
        if not authorization_header:
            return None
        elif type(authorization_header) is not str:
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        pattern = r'(?<=Basic ).+'
        match = re.findall(pattern, authorization_header)
        return match[0]

    def decode_base64_authorization_header(self,
                                           base64_d: str) -> str:
        """ decode base """
        if not base64_d:
            return None
        elif type(base64_d) is not str:
            return None
        try:
            decoded = base64.b64decode(base64_d)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_d: str) -> (str, str):
        """ exctract user credentials """
        if not decoded_base64_d:
            return (None, None)
        elif type(decoded_base64_d) is not str:
            return (None, None)
        elif ':' not in decoded_base64_d:
            return (None, None)
        return tuple(decoded_base64_d.split(':'))
