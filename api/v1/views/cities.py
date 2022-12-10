#!/usr/bin/python3
"""states module"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """Retrieve the list of all Cities of a State"""
    stt = storage.get(State, state_id)
    if not stt:
        abort(404)
    _list = []
    for obj in stt.cities:
        _list.append(obj.to_dict())
    return jsonify(_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_obj_city(city_id):
    """Retrieves a City Object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_city(city_id):
    """Delete a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_an_city(state_id):
    """Creates a City"""
    stt = storage.get(State, state_id)
    if not stt:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    data = request.get_json()
    obj = City(**data)
    obj.state_id = stt.id
    storage.new(obj)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_an_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(city, key, value)
            storage.save()
    return jsonify(city.to_dict()), 200
