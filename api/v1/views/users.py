#!/usr/bin/python3
"""states module"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieve the list of all Users"""
    _list = []
    for obj in storage.all(User).values():
        _list.append(obj.to_dict())
    return jsonify(_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_obj_users(user_id):
    """Retrieves a User Object"""
    for obj in storage.all(User).values():
        if obj.id == user_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_an_user(user_id):
    """Delete a User object"""
    for obj in storage.all(User).values():
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_an_user():
    """Creates a User"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'password' not in request.get_json():
        abort(400, "Missing password")
    if 'email' not in request.get_json():
        abort(400, "Missing email")
    data = request.get_json()
    obj = User(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_an_user(user_id):
    """Updates a User object"""
    u = storage.get(User, user_id)
    if not u:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key != "id" and key != "created_at" and\
                key != "updated_at" and key != "email":
            setattr(u, key, value)
            storage.save()
    return jsonify(u.to_dict()), 200
