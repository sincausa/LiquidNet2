"""
Exceptions
"""


class BusinessException(Exception):
    """
    Base exception for all business level errors
    """
    def __init__(self, description):
        self.description = description
        super().__init__()
