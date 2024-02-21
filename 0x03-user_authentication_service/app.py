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
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
