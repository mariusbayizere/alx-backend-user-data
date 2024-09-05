#!/usr/bin/env python3
"""
Session Authentication module
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Session authentication class that inherits from Auth.
    """

    # Class attribute to store session data
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given user_id.
        Returns:
            Session ID if successful, None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID using uuid4
        session_id = str(uuid.uuid4())

        # Store the session_id with the associated user_id in the dictionary
        self.user_id_by_session_id[session_id] = user_id
        return session_id
