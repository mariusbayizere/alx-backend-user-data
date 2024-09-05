#!/usr/bin/env python3
"""
Session Authentication module
"""
from flask import Blueprint, request, jsonify, current_app
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

        Args:
            user_id (str): The user ID for which the session is created.

        Returns:
            str: The generated session ID if successful, None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID using uuid4
        session_id = str(uuid.uuid4())

        # Store the session_id with the associated user_id in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a given Session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The User ID if found, otherwise None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.

        Args:
            request: The Flask request object.

        Returns:
            User: The User instance if found, otherwise None.
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


session_auth_views = Blueprint(
    'session_auth_views',
    __name__,
    url_prefix='/api/v1'
)


@session_auth_views.route('/auth_session/login', methods=['POST'])
def login():
    """
    Handles user login and session creation.

    Returns:
        Response: A JSON response with user details or error messages.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]  # Assuming search returns a list
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    if session_id is None:
        return jsonify({"error": "session creation failed"}), 500

    # Set the session ID cookie
    response = jsonify(user.to_json())
    response.set_cookie(current_app.config['SESSION_NAME'], session_id)

    return response
