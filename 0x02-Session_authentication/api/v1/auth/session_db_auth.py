#!/usr/bin/env python3

""" class SessionDBAuth
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    class SessionDBAuth
    """
    def create_session(self, user_id=None):
        """ create session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        dict = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**dict)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ overload user_id_for_session_id
        """
        pass

    def destroy_session(self, request=None):
        """ overload destroy session
        """
        pass
