#!/usr/bin/env python3

"""
Auth
"""

import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash password method
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)

    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register user method
        """
        try:
            # check if user already exists
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {user.email} already exists')
        except NoResultFound:
            # if no result is found, save the user
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Credentials validation
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                encoded_password = password.encode('utf-8')
                check_password = bcrypt.checkpw(encoded_password,
                                                user.hashed_password)
                if check_password:
                    return True
                return False
        except Exception:
            return False

def _generate_uuid() -> str:
    """
    Return a string representation of a new UUID
    """
    new_uuid = str(uuid.uuid4())
    return new_uuid
