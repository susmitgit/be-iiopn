from flask import Blueprint
from application.api.error_response import ErrorResponses

api = Blueprint('api_base', __name__)

from . import users, business, schedule
api_base = api


@api_base.errorhandler(400)
def bad_request():
    return ErrorResponses.bad_request()


@api_base.errorhandler(401)
@api_base.errorhandler(403)
def forbidden():
    return ErrorResponses.unauthorised_access()


@api_base.errorhandler(404)
def page_not_found():
    return ErrorResponses.not_found()


@api_base.errorhandler(405)
def method_not_allowed():
    return ErrorResponses.method_not_allowed()


@api_base.errorhandler(429)
def rate_limit(error):
    return ErrorResponses.api_rate_limit_error(message=str(error))


@api_base.errorhandler(500)
def internal_server_error(error):
    return ErrorResponses.internal_server_error(message=str(error))


@api_base.before_request
def before_request():
    pass
    # check for Idle time & expiration
    # flask.g.user = current_user
