#!/usr/bin/python3
"""Amenities api for our Airbnb"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/amenities', methods=['get'], strict_slashes=False)
def amenities_all():
    """ returns all Amenity items """
    amenities_all = []
    amenities = storage.all("Amenity").values()
    for amenity in amenities:
        amenities_all.append(amenity.to_dict())
    return jsonify(amenities_all)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_get(amenity_id):
    """ handles GET method """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity = amenity.to_dict()
    return jsonify(amenity)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenity_delete(amenity_id):
    """ handles DELETE method """
    empty_dict = {}
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    amenity = amenity.to_dict()
    return jsonify(amenity), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_put(amenity_id):
    """ handles PUT method """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            amenity.bm_update(key, value)
    amenity.save()
    amenity = amenity.to_dict()
    return jsonify(amenity), 200
