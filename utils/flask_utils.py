"""
Helpers to work with flask views
"""
from functools import wraps
from flask import (
    jsonify,
    request,
)
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import BadRequest


def validate_json(func):
    @wraps(func)
    def wrapper(*args, **kw):
        msg = "Payload must be a valid json"
        try:
            if request.json is None:
                return jsonify({"error": msg}), 422
        except BadRequest as e:
            return jsonify({"error": msg}), 422
        return func(*args, **kw)

    return wrapper


def validate_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            try:
                validate(request.json, schema, format_checker=draft7_format_checker)
            except ValidationError as e:
                return jsonify({"error": e.message}), 422
            return func(*args, **kw)

        return wrapper

    return decorator
