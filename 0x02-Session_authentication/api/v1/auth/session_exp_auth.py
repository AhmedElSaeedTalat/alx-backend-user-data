#!/usr/bin/env python3
""" setting expiration class """
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ session expiration class """
    def __init__(self):
        """ init method """
        env = getenv('SESSION_DURATION')
        if env and env.isdigit():
            self.session_duration = int(env)
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create session """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session = {}
        session['user_id'] = user_id
        session['created_at'] = datetime.now()
        self.user_id_by_session_id[session_id] = session
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ returns user """
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']
        if 'created_at' not in self.user_id_by_session_id[session_id]:
            return None
        duration = timedelta(seconds=self.session_duration)
        created_at = self.user_id_by_session_id[session_id]['created_at']
        session_expiry_time = duration + created_at
        if datetime.now() > session_expiry_time:
            return None
        return self.user_id_by_session_id[session_id]['user_id']
