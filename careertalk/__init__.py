from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
with open('config.json', 'r') as f:
    config = json.load(f)

app = Flask(__name__)

app.debug = True
app.secret_key = config['default']['secret_key']
app.config['JWT_SECRET_KEY'] = app.secret_key  # Change this!
app.config['social_facebook'] = {
    'app_id': config['social']['facebook']['app_id'],
    'app_secret': config['social']['facebook']['app_secret']
}

app.config['social_google'] = {
    'client_id': config['social']['google']['client_id'],
    'client_secret': config['social']['google']['client_secret']
}

if not app.debug:
    print('****************** DEBUG MODE ******************')
    app.config['SQLALCHEMY_DATABASE_URI'] = config['default']['local_db']
else:
    print('****************** PRODUCTION MODE ******************')
    postgres = config["postgres"]
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(
                                                    postgres["user"],
                                                    postgres["pw"],
                                                    postgres["endpoint"],
                                                    postgres["port"],
                                                    postgres["db"])

db = SQLAlchemy(app)

from careertalk import routes