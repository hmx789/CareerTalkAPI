from flask import Flask

version = '2.0.0'


def create_rest(config):
    from careertalk.views import blueprints
    from careertalk.models import db
    from flask_jwt_extended import (
        JWTManager, jwt_required, create_access_token,
        get_jwt_identity
    )

    print("CREATE REST API.")
    # TODO: In production we need one more line of code that loads
    #      environment variables and overrides the app configuration.
    app = _create_app(config)
    db.init_app(app)
    jwt = JWTManager(app)

    # register all the blueprints.
    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    return app


def _create_app(config_obj):

    """
    :param config_obj: Configuration object.

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


def create_operation(config_obj, op):
    from careertalk.models import db

    print("CREATE {} APP.".format(op))
    app = _create_app(config_obj)
    db.init_app(app)
    return app, db
