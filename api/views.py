"""
Root entry.
"""
from flask import Blueprint

general_bp = Blueprint('general', __name__)


@general_bp.route('/')
def main_entry():
    """
    Root view
    :return:
    """
    return 'LiquidNet Test'
