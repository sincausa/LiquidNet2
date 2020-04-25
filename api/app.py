"""
App factory
"""
from flask import Flask
import werkzeug
from api.db.models import db
from api.errors import handle_500, handle_404, handle_business
from api.exceptions import BusinessException
from api.user_request.views import user_request_bp
from api.views import general_bp


def create_app(config):
    """
    App Factory method
    :param Config config:
    :return: Flask app
    """
    # Required: Add Logging

    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)

    app.register_blueprint(general_bp)
    app.register_blueprint(user_request_bp)

    # error handlers
    app.register_error_handler(werkzeug.exceptions.InternalServerError, handle_500)
    app.register_error_handler(werkzeug.exceptions.NotFound, handle_404)
    app.register_error_handler(BusinessException, handle_business)

    with app.app_context():
        db.create_all()

    return app
