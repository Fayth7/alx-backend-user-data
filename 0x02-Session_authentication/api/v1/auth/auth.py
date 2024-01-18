#!/usr/bin/env python3
"""
Module for API authentication.
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    Authentication class.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if API routes require authentication.

        Parameters:
        - path (str): The API route path.
        - excluded_paths (List[str]): List of excluded paths.

        Returns:
        bool: True if authentication is required, False otherwise.
        """

        if not path or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and
            path.startswith(excluded_path[:-1]):
                return False
            elif excluded_path in {path, path + '/'}:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Checks if the Authorization request header is present

        Parameters:
        - request: The request object.

        Returns:
        str: The value of the Authorization header.
        """

        if not request or "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method.

        Parameters:
        - request: The request object.

        Returns:
        User: The current user.
        """

        return None

    def session_cookie(self, request=None):
        """
        Returns the cookie value from a request.

        Parameters:
        - request: The request object.

        Returns:
        str: The value of the session cookie.
        """

        if not request:
            return None

        return request.cookies.get(getenv('SESSION_NAME'))
