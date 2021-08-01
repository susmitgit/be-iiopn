from flask import Blueprint, jsonify, render_template

api = Blueprint('api_base', __name__)

from . import users

api_base = api

@api_base.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Forbidden'), 403

@api_base.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page Not Found'), 404

@api_base.errorhandler(405)
def method_not_allowed(error):
    return jsonify(message="Method Not Allowed for the requested URLee."), 401

@api_base.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title='Server Error'), 500

@api_base.before_request
def before_request():

    pass
    # check for Idle time & expiration
    # flask.g.user = current_user