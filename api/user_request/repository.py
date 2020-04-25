"""
Module to implement repository layer.
Usually I introduce also service level for business logic,
but because task is simple we can skip it here.
"""
import uuid
from datetime import datetime as dt
from api.db.models import db
from api.db.models import User, Title, Request
from api.exceptions import BusinessException
from api.view_models.models import VMRequest


def create_request(user_email, title):
    """
    Creates request and returns VMRequest object
    :param str user_email:
    :param str title:
    :return: VMRequest
    """
    request_id = str(uuid.uuid4())

    user_id = get_or_create_user_id_by_email(user_email)
    title_id = get_title_id_if_exists(title)
    if not title_id:
        # other way is to return Error object and check it on service/controller level
        raise BusinessException("Title not found")
    try:
        request = Request(
            id=request_id,
            user_id=user_id,
            title_id=title_id
        )
        db.session.add(request)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        # Error handling for db errors required
        # this is not good way because tech information
        # about system internal structure will be available to user
        # Also we need roundtrip for PK violation in case if our
        # generated id is duplicated or add id unique check
        raise BusinessException(str(exc))
    return VMRequest(
        request_id=request_id,
        user_id=user_id,
        user_email=user_email,
        title_id=title_id,
        title=title,
        timestamp=request.timestamp)


def get_request(request_id):
    """
    Returns request by id
    :param str request_id: Id of request
    :return: VMRequest or None
    """
    query = db.session.query(
        Request, User.email, Title.title).filter_by(id=request_id) \
        .join(User, Request.user_id == User.id) \
        .join(Title, Request.title_id == Title.id)
    request = query.first()
    return VMRequest(
        request_id=request_id,
        user_id=request.Request.user_id,
        user_email=request.email,
        title_id=request.Request.title_id,
        title=request.title,
        timestamp=request.Request.timestamp) if request else None


def get_requests_list():
    """
    Return list of request. Returns empty list if requests not found
    :return: list of VMRequest
    """
    query = db.session.query(
        Request, User.email, Title.title) \
        .join(User, Request.user_id == User.id) \
        .join(Title, Request.title_id == Title.id)
    requests = query.all()  # If amount of requests supposed to be big, we need to use paging
    return [VMRequest(
        request_id=request.Request.id,
        user_id=request.Request.user_id,
        user_email=request.email,
        title_id=request.Request.title_id,
        title=request.title,
        timestamp=request.Request.timestamp) for request in requests] if requests else []


# Methods below can be in other modules if we want to have repositories for user and title
def get_or_create_user_id_by_email(user_email):
    """
    Returns user id by email. Creates new User if user not exists
    :param user_email:
    :return:
    """
    user_id = db.session.query(User.id).filter_by(email=user_email.lower()).scalar()
    if user_id is None:
        try:
            user = User(
                id=str(uuid.uuid4()),
                email=user_email.lower(),
                created=dt.now()
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        except Exception as exc:
            db.session.rollback()
            # Normal error handling for db errors required
            raise BusinessException(str(exc))
    return user_id


def delete_request(request_id):
    """
    Deletes request
    :param str request_id:
    :return:
    """
    try:
        Request.query.filter(Request.id == request_id).delete()
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        # Normal error handling for db errors required
        raise BusinessException(str(exc))


def get_title_id_if_exists(title):
    """
    Returns title id bu title
    :param str title:
    :return: str
    """
    return db.session.query(Title.id).filter_by(title=title).scalar()
