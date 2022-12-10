#!/usr/bin/python3
"""Amenities module of the proyect Api Restfull Holberton"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieve the list of all Amenities"""
    _list = []
    for obj in storage.all(Amenity).values():
        _list.append(obj.to_dict())
    return jsonify(_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_obj_Amenity(amenity_id):
    """Retrieves a Amenity Object"""
    for obj in storage.all(Amenity).values():
        if obj.id == amenity_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_amenity(amenity_id):
    """Delete a Amenity object"""
    for obj in storage.all(Amenity).values():
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_a_amenity():
    """Creates a Amenity"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    data = request.get_json()
    obj = Amenity(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_an_amenity(amenity_id):
    """Updates a Amenity object"""
    ame = storage.get(Amenity, amenity_id)
    if not ame:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(ame, key, value)
            storage.save()
    return jsonify(ame.to_dict()), 200
