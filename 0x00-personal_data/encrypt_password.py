#!/usr/bin/env python3

"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a salted, hashed password, which is a byte string
    """
    Bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(Bytes, salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password
    """
    password_bytes = password.encode('utf-8')
    result = bcrypt.checkpw(password_bytes, hashed_password)

    return result
