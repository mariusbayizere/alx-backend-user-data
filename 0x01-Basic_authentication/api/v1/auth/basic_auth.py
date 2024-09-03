#!/usr/bin/env python3
"""This module provides an implementation of Basic Authentication for the API.
"""

import re
import base64
import binascii
from typing import Tuple, TypeVar
from .auth import Auth
from models.user import User


class BasicAuthentication(Auth):
    """A class that handles Basic Authentication for API requests.
    """

    def get_base64_authorization_token(self, auth_header: str) -> str:
        """Extracts and returns the Base64-encoded token from the
        Authorization header.

        Args:
            auth_header (str): The Authorization header.

        Returns:
            str: The Base64-encoded token or None if the header is invalid.
        """
        if auth_header is None:
            return None
        if not isinstance(auth_header, str):
            return None
        if not auth_header.startswith("Basic "):
            return None
        return auth_header[6:]

    def decode_base64_token(self, encoded_token: str) -> str:
        """Decodes the Base64 token and returns it as a UTF-8 string.

        Args:
            encoded_token (str): The Base64-encoded token.

        Returns:
            str: The decoded token in UTF-8 format or None if decoding fails.
        """
        if isinstance(encoded_token, str):
            try:
                decoded_bytes = base64.b64decode(
                    encoded_token, validate=True
                )
                return decoded_bytes.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None
        return None

    def retrieve_user_credentials(self, decoded_token: str) -> Tuple[str, str]:
        """Extracts the username and password from the decoded Base64 token.

        Args:
            decoded_token (str): The decoded token from Base64.

        Returns:
            Tuple[str, str]: The username and password, or (None, None) if
            invalid.
        """
        if isinstance(decoded_token, str):
            credentials = decoded_token.split(":", 1)
            if len(credentials) == 2:
                return credentials[0], credentials[1]
        return None, None

    def find_user_from_credentials(
            self, email: str, password: str) -> TypeVar('User'):
        """Finds a user based on the provided email and password.

        Args:
            email (str): The email of the user.
            password (str): The user's password.

        Returns:
            User: The corresponding user if the credentials are valid,
            otherwise None.
        """
        if isinstance(email, str) and isinstance(password, str):
            try:
                users = User.search({'email': email})
                if users and users[0].is_valid_password(password):
                    return users[0]
            except Exception:
                return None
        return None

    def get_authenticated_user(self, request=None) -> TypeVar('User'):
        """Retrieves the authenticated user based on the Authorization header.

        Args:
            request: The request object containing the Authorization header.

        Returns:
            User: The authenticated user object if authentication fails.
        """
        authorization_header = self.authorization_header(request)
        base64_token = self.get_base64_authorization_token(
            authorization_header)
        decoded_token = self.decode_base64_token(base64_token)
        email, password = self.retrieve_user_credentials(decoded_token)
        return self.find_user_from_credentials(email, password)
