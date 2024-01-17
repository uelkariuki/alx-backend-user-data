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
        if path[-1] != '/':
            path += '/'
        if excluded_paths[-1] != '/':
            excluded_paths += '/'

        has_star_result = [excluded_path[:-1]
                           for excluded_path in excluded_paths
                           if excluded_path[-1] == '*']
        for excluded_path in has_star_result:
            if path.startswith(excluded_path):
                return False

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method authorization_header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        # otherwise return value of header request Authorization
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """public method current_user"""
        return None
