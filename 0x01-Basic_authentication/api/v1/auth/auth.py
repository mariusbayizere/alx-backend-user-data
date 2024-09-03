#!/usr/bin/env python3
""" Authentication Module """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if the path is the list of strings excluded_paths """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Add a trailing slash to path if not present for comparison
        if not path.endswith('/'):
            path += '/'

        # Check if the path is in excluded_paths
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                if path == excluded_path:
                    return False

        return True
