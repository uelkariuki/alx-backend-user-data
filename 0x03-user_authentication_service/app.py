#!/usr/bin/env python3

"""
Flask app
"""

from flask import Flask, jsonify, request
from auth import Auth, _hash_password
from user import User

app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def message():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """
    End-point to register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        new_user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": f"{new_user.email}",
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
