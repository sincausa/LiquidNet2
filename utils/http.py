from flask import jsonify


def response_ok(data=None):
    resp = jsonify(data if data else {})
    resp.status_code = 200 if data else 204
    return resp


def response_error(status_code, data):
    """
    Custom handler for any errors
    :param int status_code:
    :param object data:
    :return:
    """
    message = {
        'status': status_code,
        'error_data': data,
    }
    resp = jsonify(message)
    resp.status_code = status_code
    return resp


def validation_error(data):
    response_error(422, data)