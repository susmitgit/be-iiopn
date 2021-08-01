from flask import Flask, render_template

def create_app(config_name):
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    return app