#!/usr/bin/python3
"ssssssssssssssssssssssssssssssssss"
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns status of api"""
    final = {}
    items = [
            'Amenities',
            'Cities',
            'Places',
            'Reviews',
            'States',
            'Users',
        ]
    for item in items:
        num = storage.count(item)
        final[item.lower()] = num
    return jsonify(final)
