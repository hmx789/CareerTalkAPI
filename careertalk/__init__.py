from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from common.config import Config, GoogleSocialLoginConfig

app = Flask(__name__)
config = Config()
version = config.VERSION

app.config.from_object(config)

print('****************** LOCAL DEV MODE ******************')
db = SQLAlchemy(app)
jwt = JWTManager(app)
google_config = GoogleSocialLoginConfig()

# build scheduler


