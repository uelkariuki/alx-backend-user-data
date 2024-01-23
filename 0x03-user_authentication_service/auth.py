#!/usr/bin/env python3

"""
Auth
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash password method
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)

    return hash
