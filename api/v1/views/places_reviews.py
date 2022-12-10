#!/usr/bin/python3
"""reviews module of the project"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_all_review(place_id):
    """Retrieve the list of all Reviews"""
    _list = []
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    for review in places.reviews:
        _list.append(review.to_dict())
    return jsonify(_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_obj_review(review_id):
    """Retrieves a Review Object"""
    for obj in storage.all(Review).values():
        if obj.id == review_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_review(review_id):
    """Delete a Review object"""
    for obj in storage.all(Review).values():
        if obj.id == review_id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_a_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, "Missing user_id")
    if 'text' not in request.get_json():
        abort(400, "Missing text")
    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    obj = Place(**data)
    storage.new(obj)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_a_review(review_id):
    """Updates a Review object"""
    stt = storage.get(Review, review_id)
    if not stt:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at"\
                and key != "user_id" and key != "place_id":
            setattr(stt, key, value)
            storage.save()
    return jsonify(stt.to_dict()), 200
