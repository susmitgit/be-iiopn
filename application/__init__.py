import os
from flask import Flask, render_template
from flask_bcrypt import Bcrypt

from config import app_config

bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    bcrypt.init_app(app)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/<path:path>', methods=['GET'])
    def any_root_path(path):
        return render_template('index.html')

    @app.errorhandler(500)
    def internal_server_error(error):
        pass
        return render_template('errors/500.html', title='Server Error'), 500

    from .api import api as api_base
    app.register_blueprint(api_base, url_prefix='/api/v1')

    return app