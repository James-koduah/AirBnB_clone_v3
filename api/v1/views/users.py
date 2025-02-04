#!/usr/bin/python3
"""
View for Users that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_all():
    """ returns list of all User objects """
    users_all = []
    users = storage.all("User")
    for k, user in users.items():
        users_all.append(user.to_dict())
    return jsonify(users_all)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_get(user_id):
    """ handles GET method """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user = user.to_dict()
    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    """ handles DELETE method """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    user = user.to_dict()
    return jsonify(user), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """ handles PUT method """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "email", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    user = user.to_dict()
    return jsonify(user), 200
