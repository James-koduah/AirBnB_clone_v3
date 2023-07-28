"""sssssssssssssssssssssssssss"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['get', 'post'])
def states_all():
    """Returns all state items"""
    if request.method == 'GET':
        all_states = []
        raw = storage.all('State')
        for k, state in raw.items():
            state = state.to_dict()
            all_states.append(state)
        return jsonify(all_states)

    if request.method == 'POST':
        client_message = request.get_json()
        if client_message is None:
            abort(400, "Not a JSON")
        if 'name' not in client_message:
            abort(400, "Missing name")
        state = State(**client_message)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['get', 'delete', 'put'])
def state_item(state_id):
    """Returns a single state item"""
    if request.method == 'GET':
        state = storage.get('State', state_id)
        if state is None:
            abort(404)
        state = state.to_dict()
        return jsonify(state)

    if request.method == 'DELETE':
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        state = storage.get('State', state_id)
        if state is None:
            abort(404)
        client_message = request.get_json()
        if client_message is None:
            abort(400, "Not a JSON")
        ignore_keys = ['id', 'created_at', 'updated_at']
        for k, v in client_message.items():
            if k not in ignore_keys:
                setattr(state, k, v)
        storage.save()
        return jsonify(state.to_dict()), 200
