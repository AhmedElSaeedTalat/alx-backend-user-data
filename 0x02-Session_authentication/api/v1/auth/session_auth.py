#!/usr/bin/env python3
""" BasicAuth to be used here """
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ session Auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ function to create session """
        if not user_id or type(user_id) is not str:
            return None
        id = str(uuid.uuid4())
        self.user_id_by_session_id[id] = user_id
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ retrieve user_id id by session id """
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ return current user
            Args
                request: received request object
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.search({'id': user_id})
        if user:
            return user[0]
        else:
            return None
