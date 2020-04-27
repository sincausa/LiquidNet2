"""
I will test only request_add method to save time
"""
import unittest
import uuid
from datetime import datetime as dt
from unittest import mock

from api.app import create_app
from api.view_models.models import VMRequest


class RequestViewsTests(unittest.TestCase):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    temp_uuid_str = str(uuid.uuid4())

    def setUp(self):
        self.app = create_app(self).test_client()

    @mock.patch('api.user_request.views.create_request', mock.MagicMock(return_value=VMRequest(
        temp_uuid_str, temp_uuid_str, 'title1', temp_uuid_str, 'email@email.com', dt.now())))
    def test_request_add_success(self):
        response = self.app.post(
            '/request',
            json={
                'email': 'email@email.com',
                'title': 'title1',
            },
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['request_id'], self.temp_uuid_str)

    # Even decorators are responsible for validation
    # we need to check it here to understand that our json scheme is correct
    def test_request_add_incorrect_email(self):
        response = self.app.post(
            '/request',
            data={
                'email': 'email',
                'title': 'book title',
            },
            follow_redirects=True)
        self.assertEqual(422, response.status_code)

    def test_request_add_no_title(self):
        response = self.app.post(
            '/request',
            data={
                'email': 'email',
            },
            follow_redirects=True)
        self.assertEqual(422, response.status_code)

    def test_request_add_no_email(self):
        response = self.app.post(
            '/request',
            data={
                'title': 'book title',
            },
            follow_redirects=True)
        self.assertEqual(422, response.status_code)

    def test_request_add_incorrect_json(self):
        response = self.app.post(
            '/request',
            data=None,
            follow_redirects=True)
        self.assertEqual(422, response.status_code)