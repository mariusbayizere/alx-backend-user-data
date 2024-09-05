#!/usr/bin/env python3
"""
Session Authentication module
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


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

        # Return the generated session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a given Session ID.
        Args:
            session_id (str): The session ID.
        Returns:
            The User ID if found, otherwise None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve the user ID using .get() to handle missing keys gracefully
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.
        Args:
            request: The Flask request object.
        Returns:
            The User instance if found, otherwise None.
        """
        # Retrieve the session ID from the cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        # Get the user ID using the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # Retrieve the User instance from the database using the user ID
        return User.get(user_id)
