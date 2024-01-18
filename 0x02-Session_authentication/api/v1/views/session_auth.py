#!/usr/bin/env python3

"""
Module of SessionAuth views that handles all routes for the Session
authentication
"""

from api.v1.views import app_views
import os
from flask import request, jsonify, session, abort
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login() -> str:
    """ POST /api/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        else:
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            session_name = os.getenv('SESSION_NAME')
            response = jsonify(user.to_json())
            response.set_cookie(session_name, session_id)
            return response


@app_views.route('auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ DELETE /api/v1/auth_session/logout
      - Deletes the user session /logout
    """
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)

    if destroy_session is False:
        abort(404)
    else:
        return jsonify({}), 200
