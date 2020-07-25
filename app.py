from flask import Flask, app
from flask_restful import Api
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from routes.main import get_routes
import os

def setup_app(config: dict = None) -> app.Flask:
    """
    Initializes Flask app with given configuration.
    Main entry point for wsgi (gunicorn) server.
    :param config: Configuration dictionary
    :return: app
    """
    # init flask
    flask_app = Flask(__name__)

    # default mongodb configuration
    default_config = {'MONGODB_SETTINGS': {
                        'host': 'mongodb://localhost:27017/ease_mart',
                        'authentication_source': 'admin'
                        },
                        'JWT_SECRET_KEY': 'secretTest'
                      }

    # configure app
    config = default_config if config is None else config
    flask_app.url_map.strict_slashes = False
    flask_app.config.update(config)

    # load config variables
    if 'MONGODB_URI' in os.environ:
        flask_app.config['MONGODB_SETTINGS'] = {'host': os.environ['MONGODB_URI'], 'retryWrites': False}
    if 'JWT_SECRET_KEY' in os.environ:
        flask_app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

    # init api and routes
    api = Api(app=flask_app)
    get_routes(api=api)
    # init mongoengine
    MongoEngine(app=flask_app)
    # init jwt manager
    JWTManager(app=flask_app)

    return flask_app

if __name__ == '__main__':
    app=setup_app()
    app.run(debug=True)