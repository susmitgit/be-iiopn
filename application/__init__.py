import logging
import os
from flask import Flask, render_template, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from config import app_config
from application.api_conf.api_config import ApiConfig

from application.api.error_response import ErrorResponses

bcrypt = Bcrypt()


def create_app(config_name):

    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/', instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    bcrypt.init_app(app)
    limiter = ApiConfig.init_rate_limit(app_instance=app)
    ApiConfig.init_log(config_name=config_name)

    @app.route('/', methods=['GET'])
    @limiter.limit("1000/minute")
    def index(path=''):
        if path and path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>', methods=['GET'])
    def any_root_path():
        return 'Is it open? API working fine'

    @app.errorhandler(500)
    def internal_server_error(error):
        logging.error(str(error))
        return ErrorResponses.internal_server_error(message=str(error))

    @app.errorhandler(429)
    def api_rate_limit(error):
        logging.error(str(error))
        return ErrorResponses.api_rate_limit_error(message=str(error))

    @app.errorhandler(405)
    def method_not_allowed(error):
        logging.error(str(error))
        return ErrorResponses.method_not_allowed()

    from .api import api as api_base
    app.register_blueprint(api_base, url_prefix='/api/v1')

    return app
