#!/usr/bin/env python3

"""
Basic auth class that inherits from Auth
"""

import base64
import binascii
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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None

        base64_authorization_header = check_if_valid_base64(
            base64_authorization_header)
        if base64_authorization_header is None:
            return None

        base64string = base64_authorization_header.encode().decode('utf-8')
        decoded_bytes = base64.b64decode(base64string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is int or ':' not in\
                decoded_base64_authorization_header:
            return (None, None)
        else:
            # user_details entails the user email and password
            user_details = tuple(decoded_base64_authorization_header.split(
                ':'))
            return user_details


def check_if_valid_base64(base64_authorization_header):
    """ Checks if header is a valid base64 string
    """
    try:
        base64.b64decode(base64_authorization_header)
        return base64_authorization_header
    except binascii.Error:
        # if error is raised it is not a valid Base64 String
        return None
