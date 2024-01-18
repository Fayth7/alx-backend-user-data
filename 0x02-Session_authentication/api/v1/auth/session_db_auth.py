#!/usr/bin/env python3
"""
Module for API session database authentication.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """
    Session Database Authentication class.
    """

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for the provided user_id.

        Parameters:
        - user_id (str): The user ID.

        Returns:
        str: The generated session ID.
        """
        pass

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the User ID based on the Session ID.

        Parameters:
        - session_id (str): The session ID.

        Returns:
        str: The user ID.
        """
        if not session_id or not isinstance(session_id, str):
            return None
        else:
            pass

    def destroy_session(self, request=None):
        """
        Deletes the user session to log out.

        Parameters:
        - request: The request object.
        """
        pass
