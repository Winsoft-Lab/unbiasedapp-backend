from app.exceptions import ValidationError
from flask import request, jsonify, render_template
from . import api
from werkzeug.http import HTTP_STATUS_CODES


def forbiden(message):
    response = jsonify({"error": "forbidden", "message": message})
    response.status_code = 403
    return response


def unauthenticated(message):
    response = jsonify({"error": "unauthenticated", "message": message})
    response.status_code = 401
    return response


def error_response(status_code, message=None):
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unkown error")}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    pass  # bad_request(e.args[0])
