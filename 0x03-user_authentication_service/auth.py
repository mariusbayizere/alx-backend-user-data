#!/usr/bin/env python3
"""
Auth module to handle user authentication and registration.
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt, checkpw


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initializes the Auth class with a DB instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user by adding their email and hashed password
        to the database.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If user does not exist, create a new user
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email,
                                         hashed_password.decode('utf-8'))
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            # Check if the provided password matches the stored hashed password
            if checkpw(password.encode('utf-8'),
                       user.hashed_password.encode('utf-8')):
                return True
            return False
        except NoResultFound:
            return False
