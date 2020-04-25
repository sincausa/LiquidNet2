import unittest
from unittest import mock

from flask import Flask
from werkzeug.exceptions import BadRequest

from utils.flask_utils import validate_json, validate_schema


@validate_json
def test_method_json():
    return True


@validate_schema({
    "type" : "object",
    "required": ["a"],
    "properties": {
        "a": {"type": "string"},
        "b": {"type": "string", 'format': 'email'},
 }})
def test_method_schema():
    return True


class ValidateJsonTests(unittest.TestCase):

    def test_validate_json_success(self):
        with Flask(__name__).test_request_context("/hello", json={'a': 1}):
            self.assertTrue(test_method_json())

    def test_validate_json_none_json_request(self):
        with Flask(__name__).test_request_context("/hello"):
            self.assertEqual(422, test_method_json()[1])


class ValidateSchemaTests(unittest.TestCase):

    def test_validate_schema_success(self):
        flask_request = mock.MagicMock()
        flask_request.json = {}
        with Flask(__name__).test_request_context("/hello", json={'a': '1', 'b': 'email@em.co'}):
            self.assertTrue(test_method_schema())

    def test_validate_schema_success_required_only(self):
        flask_request = mock.MagicMock()
        flask_request.json = {}
        with Flask(__name__).test_request_context("/hello", json={'a': '1'}):
            self.assertTrue(test_method_schema())

    def test_validate_schema_required_missed(self):
        with Flask(__name__).test_request_context("/hello", json={'b': 'email@em.co'}):
            self.assertEqual(422, test_method_schema()[1])

    def test_validate_schema_wrong_email_format(self):
        with Flask(__name__).test_request_context("/hello", json={'a': 1, 'b': '1'}):
            self.assertEqual(422, test_method_schema()[1])
