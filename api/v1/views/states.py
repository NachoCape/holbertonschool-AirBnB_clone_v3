#!/usr/bin/python3
"""states module"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieve the list of all States"""
    _list = []
    for obj in storage.all(State).values():
        _list.append(obj.to_dict())
    return jsonify(_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_obj_states(state_id):
    """Retrieves a State Object"""
    for obj in storage.all(State).values():
        if obj.id == state_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_an_obj(state_id):
    """Delete a State object"""
    for obj in storage.all(State).values():
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_an_obj():
    """Creates a state"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    data = request.get_json()
    obj = State(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_an_obj(state_id):
    """Updates a State object"""
    stt = storage.get(State, state_id)
    if not stt:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(stt, key, value)
            storage.save()
    return jsonify(stt.to_dict()), 200
