#!/usr/bin/env python3

""" Class to manage the API authentication
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """"Manage API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method require_auth"""
        if excluded_paths is None or path is None:
            return True
        if len(excluded_paths) == 0:
            return True
        normal_path = path.rstrip('/')
        normal_excluded_path = [p.rstrip('/') for p in excluded_paths]

        if normal_path in normal_excluded_path:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method authorization_header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        # otherwise return value of header request Authorization
        auth_value = request.headers.get('Authorization')
        return auth_value

    def current_user(self, request=None) -> TypeVar('User'):
        """public method current_user"""
        return None
