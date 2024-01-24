#!/usr/bin/env python3

"""
Flask app
"""

from flask import Flask, jsonify, make_response, redirect, request, abort
from auth import Auth, _hash_password

app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def message() -> str:
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
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


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user or not session_id:
        abort(403)
    if user:
        return jsonify({"email": f"{user.email}"}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ POST /reset_password
    """
    try:
        email = request.form.get('email')

        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email,
                        "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ PUT /reset_password
    """
    user_email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": user_email,
                        "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
