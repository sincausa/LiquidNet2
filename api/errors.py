"""
Error handlers
"""
from utils.http import response_error


def handle_500(error):
    """
    500 error
    :param error:
    :return:
    """
    original = getattr(error, "original_exception", None)

    if original is None:
        return response_error(500)

    return response_error(500, original)


def handle_404(error):
    """
    400 error
    :param error:
    :return:
    """
    return response_error(404, {'desc': error.description})


def handle_business(error):
    """
    Subsystem of our exceptions for business logic
    :param error:
    :return:
    """
    return response_error(424, {'desc': error.description})
