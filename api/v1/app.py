#!/usr/bin/python3
"""Flask application api"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    try:
        host = os.environ.get('HBNB_API_HOST')
    except Execption as e:
        host = '0.0.0.0'

    try:
        port = os.environ.get('HBNB_API_PORT')
    except Execption as e:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
