#!/usr/bin/env python3
""" flask app """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
