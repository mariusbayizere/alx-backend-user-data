#!/usr/bin/env python3
""" Authentication Module """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a path requires authentication """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns None - for now the request will be handled later """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None - user to be handled later """
        return None
