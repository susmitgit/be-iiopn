import os
import logging

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import app_config

bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    bcrypt.init_app(app)
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["2000/day", "300/hour", "50/minute"]
    )
    log_level = logging.DEBUG
    if app_config[config_name] == 'production':
        log_level = logging.ERROR

    logging.basicConfig(filename='logs/be_server.log', level=log_level,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    @app.route('/', methods=['GET'])
    @limiter.limit("10/minute")
    def index():
        logging.info("Hitting Root")
        return render_template('index.html')

    @app.route('/<path:path>', methods=['GET'])
    def any_root_path(path):
        return render_template('index.html')

    @app.errorhandler(500)
    def internal_server_error(error):
        logging.error(str(error))
        return render_template('errors/500.html', title='Server Error'), 500

    from .api import api as api_base
    app.register_blueprint(api_base, url_prefix='/api/v1')

    return app