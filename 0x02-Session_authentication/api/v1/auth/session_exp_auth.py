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
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dictionary

        # self.user_id_by_session_id[user_id] = user_id
        # self.user_id_by_session_id[created_at] = datetime.now()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Overload user_id_for_session_id
        """
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        user_id = session_dictionary.get('user_id')
        if self.session_duration <= 0:
            return user_id
        created_at = session_dictionary.get('created_at')
        allow_window = created_at + timedelta(seconds=self.session_duration)
        if created_at not in session_dictionary.keys():
            return None
        if allow_window < datetime.now():
            return None

        return user_id
