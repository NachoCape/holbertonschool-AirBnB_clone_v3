#!/usr/bin/python3
"""places module of the project"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieve the list of all Places"""
    _list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city:
        _list.append(place.to_dict())
    return jsonify(_list)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_obj_places(place_id):
    """Retrieves a Place Object"""
    for obj in storage.all(Place).values():
        if obj.id == place_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_an_obj(place_id):
    """Delete a Place object"""
    for obj in storage.all(Place).values():
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_an_obj(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, "Missing user_id")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    obj = Place(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_an_obj(place_id):
    """Updates a Place object"""
    stt = storage.get(Place, place_id)
    if not stt:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at"\
                and key != "user_id" and key != "city_id":
            setattr(stt, key, value)
            storage.save()
    return jsonify(stt.to_dict()), 200
