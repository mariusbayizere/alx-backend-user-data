#!/usr/bin/env python3
""" Authentication Module """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if the path requires authentication """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Add a trailing slash to path if not present for comparison
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                # Match the beginning of the path with the excluded path
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                if excluded_path.endswith('/'):
                    if path == excluded_path:
                        return False
                elif path.rstrip('/') == excluded_path.rstrip('/'):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the value of the Authorization header if present """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')
