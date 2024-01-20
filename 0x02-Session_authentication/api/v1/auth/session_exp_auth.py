#!/usr/bin/env python3

""" Add an expiration date to a Session ID
"""

from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ class SessionExpAuth that inherits from SessionAuth
    """
    def __init__(self):
        """ overload initialization
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Overload create session method
        """
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None

        user_details = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        self.user_id_by_session_id[session_id] = user_details

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Overload user_id_for_session_id
        """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if "created_at" not in user_details.keys():
            return None
        user_id = user_details.get('user_id')
        if self.session_duration <= 0:
            return user_id

        created_at = user_details.get('created_at')

        allow_window = created_at + timedelta(seconds=self.session_duration)
        if allow_window < datetime.now():
            return None

        return user_id
