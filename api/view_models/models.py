"""
View models
"""


class JsonSerializable:
    """
    Base class for View Model objects
    """
    def to_dict(self):
        """ it's not implementation. just temporary fast approach """
        return self.__dict__


# pylint: disable=too-many-arguments
class VMRequest(JsonSerializable):
    """
    ViewModel for Request objects
    """
    def __init__(self, request_id, title_id, title, user_id, user_email, timestamp):
        """
        Constructor
        :param str request_id:
        :param str title_id:
        :param str title:
        :param str user_id:
        :param str user_email:
        :param datetime.datetime timestamp:
        """
        self.request_id = request_id
        self.title_id = title_id
        self.title = title
        self.user_id = user_id
        self.email = user_email
        self.timestamp = timestamp.isoformat()
