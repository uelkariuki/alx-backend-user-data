#!/usr/bin/env python3

"""
Basic auth class that inherits from Auth
"""

from flask import request
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Class BasicAuth that inherits from Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header for a Basic
        Authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if 'Basic ' not in authorization_header:
            return None
        else:
            return authorization_header.split('Basic ')[1]
