from flask import Blueprint
from application.api.error_response import ErrorResponses

api = Blueprint('api_base', __name__)

from . import users, business, schedule


api_base = api

@api_base.errorhandler(403)
def forbidden(error):
    return ErrorResponses.unauthorised_access()

@api_base.errorhandler(404)
def page_not_found(error):
    return ErrorResponses.not_found()

@api_base.errorhandler(405)
def method_not_allowed(error):
    return ErrorResponses.method_not_allowed()

@api_base.errorhandler(500)
def internal_server_error(error):
    return ErrorResponses.internal_server_error()

@api_base.before_request
def before_request():
    pass
    # check for Idle time & expiration
    # flask.g.user = current_user
