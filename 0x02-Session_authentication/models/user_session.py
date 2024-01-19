#!/usr/bin/env python3

""" UserSession
"""
from models.base import Base


class UserSession(Base):
    """ class UserSession
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ initialize
        """
        super().init(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
