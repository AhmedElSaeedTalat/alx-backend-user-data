#!/usr/bin/env python3
"""
Main file
"""
import requests
import json


base_url = 'http://localhost:5000'
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ function to register user """
    url = base_url + '/users'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    expected_response = {"email": email, "message": "user created"}
    assert response.status_code == 200
    assert json.loads(response.text) == expected_response


def log_in_wrong_password(email: str, password: str) -> None:
    """ check wrong passwords """
    url = base_url + '/sessions'
    data = {'email': email, 'password': 'fake password'}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ log in """
    url = base_url + '/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    expected_response = {"email": email, "message": "logged in"}
    cookies = response.cookies
    session_id = cookies.get('session_id')
    assert response.status_code == 200
    assert json.loads(response.text) == expected_response
    return session_id


def profile_unlogged() -> None:
    """ profile unlogged """
    url = base_url + '/profile'
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ profile logged """
    url = base_url + '/profile'
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    expected_response = {"email": "guillaume@holberton.io"}
    assert response.status_code == 200
    assert json.loads(response.text) == expected_response


def log_out(session_id: str) -> None:
    """ log out """
    url = base_url + '/sessions'
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies, allow_redirects=False)
    assert response.status_code == 302


def reset_password_token(email: str) -> str:
    """ reset password """
    url = base_url + '/reset_password'
    data = {'email': email}
    response = requests.post(url, data)
    assert response.status_code == 200
    token = json.loads(response.text)['reset_token']
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ update password test """
    url = base_url + '/reset_password'
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    response = requests.put(url, data=data)
    expected_response = {"email": email, "message": "Password updated"}
    assert response.status_code == 200
    assert response.json() == expected_response


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
