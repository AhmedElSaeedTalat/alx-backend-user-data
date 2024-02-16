#!/usr/bin/env python3
""" session authentication view """
from api.v1.views import app_views
from flask import request, jsonify
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """ login function """
    from models.user import User
    from api.v1.app import auth

    email = request.form.get('email')
    if not email:
        response = jsonify({"error": "email missing"})
        response.status_code = 400
        return response
    password = request.form.get('password')
    if not password:
        response = jsonify({"error": "password missing"})
        response.status_code = 400
        return response
    users = User.search({'email': email})

    if not users:
        response = jsonify({"error": "no user found for this email"})
        response.status_code = 404
        return response

    if not users[0].is_valid_password(password):
        response = jsonify({"error": "wrong password"})
        response.status_code = 401
        return response

    user = users[0]

    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())

    response.set_cookie(getenv('SESSION_NAME'), session_id)

    return response
