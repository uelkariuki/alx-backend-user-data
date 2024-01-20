#!/usr/bin/env python3

""" class SessionDBAuth
"""

from datetime import timedelta
import datetime
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    class SessionDBAuth
    """
    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession and returns the
        Session ID
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
        Returns the User ID by requesting UserSession in the database
        based on session_id
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})

        if self.session_duration <= 0:
            return user_sessions[0].user_id
        created_at = user_sessions[0].created_at
        if (created_at +
            timedelta(seconds=self.session_duration)) < datetime.utcnow():
            return None
        return user_sessions[0].user_id


    def destroy_session(self, request=None):
        """ overload destroy session
        Destroys the UserSession based on the Session ID from the request
        cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({'session_id': session_id})
        del self.user_id_by_session_id[session_id]
        user_session[0].remove()
        return True
