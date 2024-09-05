#!/usr/bin/env python3
"""
Users views for API.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route(
   '/api/v1/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Get all users """
    users = [
        user.to_dict()
        for user in storage.all(User).values()
    ]
    return jsonify(users)


@app_views.route(
   '/api/v1/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Get a specific user by ID """
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_dict())

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())
