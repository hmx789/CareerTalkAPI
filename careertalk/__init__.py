from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

version = '2.0.0'
print('****************** LOCAL DEV MODE ******************')
jwt = JWTManager()
db = SQLAlchemy()


def create_rest(config):
    print("CREATE REST API.")
    # TODO: In production we need one more line of code that loads
    #      environment variables and overrides the app configuration.
    app = create_app(config)
    jwt.init_app(app)
    db.init_app(app)

    from careertalk.main import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def create_app(config_obj):
    print("CREATE APP.")
    """
    A factory function for generating differnt versions of app. We want many versions of app
    with different configurations depending on where we are deploying apps. This allow us to
    create multiple versions of app easily. For example, we will pass testing configuration
    into this function and create app for testing.
    :param config: config object.
    :return: flask app
    """
    app = Flask(__name__)
    app.config.from_object(config_obj)

    return app


def create_load(config_obj):
    app = create_app(config_obj)
    db.init_app(app)

    return app


def create_ingest(config_obj):
    app = create_app(config_obj)
    return app
