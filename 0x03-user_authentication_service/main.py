#!/usr/bin/env python3
""" End-to-end integration test"""

import requests

BASE_URL = 'http://localhost:5000'
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def test_register_user():
    """Test for validating user registration"""
    data = {"email": EMAIL, "password": PASSWD}
    response = requests.post(f'{BASE_URL}/users', data=data)

    msg = {"email": EMAIL, "message": "user created"}
    assert response.status_code == 200 and response.json() == msg


def test_log_in_with_wrong_password():
    """Test for validating login with wrong password"""
    data = {"email": EMAIL, "password": NEW_PASSWD}
    response = requests.post(f'{BASE_URL}/sessions', data=data)

    assert response.status_code == 401


def test_profile_unlogged():
    """Test for validating profile request without log in"""
    cookies = {"session_id": ""}
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)

    assert response.status_code == 403


def test_profile_logged():
    """Test for validating profile request when logged in"""
    session_id = log_in()
    cookies = {"session_id": session_id}
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)

    msg = {"email": EMAIL}
    assert response.status_code == 200 and response.json() == msg


def test_log_out():
    """Test for validating log out endpoint"""
    session_id = log_in()
    cookies = {"session_id": session_id}
    response = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)

    msg = {"message": "Bienvenue"}
    assert response.status_code == 200 and response.json() == msg


def test_reset_password_token():
    """Test for validating password reset token"""
    data = {"email": EMAIL}
    response = requests.post(f'{BASE_URL}/reset_password', data=data)

    assert response.status_code == 200
    reset_token = response.json().get("reset_token")

    msg = {"email": EMAIL, "reset_token": reset_token}
    assert response.json() == msg

    return reset_token


def test_update_password():
    """Test for validating password reset (update)"""
    reset_token = test_reset_password_token()
    data = {"email": EMAIL, "reset_token": reset_token,
            "new_password": NEW_PASSWD}
    response = requests.put(f'{BASE_URL}/reset_password', data=data)

    msg = {"email": EMAIL, "message": "Password updated"}
    assert response.status_code == 200 and response.json() == msg


def log_in():
    """Helper function for logging in"""
    data = {"email": EMAIL, "password": PASSWD}
    response = requests.post(f'{BASE_URL}/sessions', data=data)

    msg = {"email": EMAIL, "message": "logged in"}
    assert response.status_code == 200 and response.json() == msg

    session_id = response.cookies.get("session_id")
    return session_id


if __name__ == "__main__":
    # Run the tests
    test_register_user()
    test_log_in_with_wrong_password()
    test_profile_unlogged()
    test_profile_logged()
    test_log_out()
    test_update_password()
    test_log_in()
