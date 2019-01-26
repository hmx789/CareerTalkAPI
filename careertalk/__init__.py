from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
db = SQLAlchemy(app)
app.debug = True

with open('config.json', 'r') as f:
    config = json.load(f)

if app.debug:
    app.config['SQLALCHEMY_DATABASE_URI'] = config['default']['local_db']
else:
    postgres = config["postgres"]
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(
                                                    postgres["user"],
                                                    postgres["pw"],
                                                    postgres["endpoint"],
                                                    postgres["port"],
                                                    postgres["db"])

from careertalk import routes