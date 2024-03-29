#!/usr/bin/env python3
""" flask app """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
AUTH = Auth()
app = Flask("__name__")


@app.route('/', methods=['GET'])
def home():
    """ home function """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def add_users():
    """ post method to register users """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        if user:
            return jsonify({"email": "{}".format(email),
                            "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def create_session():
    """ creates session to user if exists"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": "{}".format(email),
                            "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ destroys session """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ profile method """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": "{}".format(user.email)}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    """ reset password api """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        res = {"email": "{}".format(email), "reset_token": "{}".format(token)}
        return jsonify(res), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ update password """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        response = {"email": "{}".format(email), "message": "Password updated"}
        return jsonify(response), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
