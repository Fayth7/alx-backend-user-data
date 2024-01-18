#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

AUTH_TYPE_MAP = {
    'basic_auth': 'api.v1.auth.basic_auth.BasicAuth',
    'session_auth': 'api.v1.auth.session_auth.SessionAuth',
    'session_exp_auth': 'api.v1.auth.session_exp_auth.SessionExpAuth',
    'session_db_auth': 'api.v1.auth.session_db_auth.SessionDBAuth',
    'default_auth': 'api.v1.auth.auth.Auth'
}

auth_type = getenv("AUTH_TYPE", 'default_auth')
auth_class = AUTH_TYPE_MAP.get(auth_type, AUTH_TYPE_MAP['default_auth'])

try:
    auth = eval(auth_class)()
except ImportError:
    raise ImportError(f"Error importing {auth_class}")

EXCLUDED_PATHS = [
    '/api/v1/status/',
    '/api/v1/unauthorized/',
    '/api/v1/forbidden/',
    '/api/v1/auth_session/login/'
]


def check_authorization(request):
    """Check if request needs authorization"""
    if auth and auth.require_auth(request.path, EXCLUDED_PATHS):
        if auth.authorization_header(request) is None and auth.session_cookie(
                request) is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)
        request.current_user = auth.current_user(request)


@app.before_request
def request_filter() -> None:
    """Filter requests"""
    check_authorization(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", "5000"))
    app.run(host=host, port=port)
