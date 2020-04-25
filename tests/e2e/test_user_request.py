import unittest
from api.app import create_app



class RequestViewsTests(unittest.TestCase):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def setUp(self):
        self.app = create_app(self).test_client()

    def test_request_add_correct(self):
        response = self.app.post(
            '/request',
            json={
                'email': 'email@email.com',
                'title': 'title1',
            },
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        #We need allso to check data in respose.json and db