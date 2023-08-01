#!/usr/bin/python3
"""sssssssssssssssssssssssssss"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['get', 'post'], 
                 strict_slashes=False)
def get_state_cities(state_id):
    """get cities of a state"""
    state = storage.get('State', state_id)
    if state == None:
        abort(404)

    if request.method == 'GET':
        all_cities = []
        cities = state.cities
        for city in cities:
            all_cities.append(city.to_dict())
        return jsonify(all_cities)
    
    if request.method == 'POST':
        client_message = request.get_json()
        if client_message is None or 'name' not in client_message:
            abort(400, "Not a JSON")
        city = City(**client_message)
        city.state_id = state_id
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['get', 'delete', 'put'],
                 strict_slashes=False)
def get_city(city_id):
    """get a city"""
    city = storage.get('City', city_id)
    if city == None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())
    
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        client_message = request.get_json()
        if client_message is None:
            abort(400, "Not a JSON")
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for k, v in client_message.items():
            if k not in ignore_keys:
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200

