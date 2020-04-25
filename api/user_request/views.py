"""
User requests views
"""
from flask import request, Blueprint
from api.user_request.repository import create_request,\
    get_request, delete_request, get_requests_list
from utils.flask_utils import validate_json, validate_schema
from utils.http import response_ok, response_error

user_request_bp = Blueprint('user_request', __name__)


@user_request_bp.route('/request/<string:request_id>', methods=['GET'])
def request_get(request_id):
    """
    Returns Request object by id
    :param request_id:
    :return:
    """
    res = get_request(request_id)
    if res:
        return response_ok(res.to_dict())
    return response_error(404, {'message': 'Request not found'})


@user_request_bp.route('/request', methods=['GET'])
def request_get_list():
    """
    Returns list of requests
    :return:
    """
    res = get_requests_list()
    return response_ok([r.to_dict() for r in res])


@user_request_bp.route('/request', methods=['POST'])
@validate_json
@validate_schema(
    {
        "type": "object",
        "required": ["title", "email"],
        "properties": {
            "title": {"type": "string"},
            "email": {"type": "string", 'format': 'email'},
        }})
def request_add():
    """
    Adds new request
    :return:
    """
    content = request.json
    data = create_request(content['email'], content['title'])
    return response_ok(data.to_dict())


@user_request_bp.route('/request/<string:request_id>', methods=['DELETE'])
def request_delete(request_id):
    """
    Delete request
    :param request_id:
    :return:
    """
    delete_request(request_id)
    return response_ok()
