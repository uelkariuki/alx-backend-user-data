#!/usr/bin/env python3

"""
Flask app
"""

from flask import Flask, jsonify, make_response, redirect, request, abort
from auth import Auth, _hash_password

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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ POST /sessions
    """
    email = request.form.get('email')
    password = request.form.get('password')

    valid_user = AUTH.valid_login(email=email, password=password)
    if not valid_user:
        abort(401)
    else:
        session_id = AUTH.create_session(email=email)
        response = make_response(jsonify({"email": email,
                                          "message": "logged in"}))
        response.set_cookie("session_id", session_id)
        return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /sessions
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
