from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configs import constants
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler

import json
with open(constants.CONFIG, 'r') as f:
    config = json.load(f)

app = Flask(__name__)

app.debug = True
app.secret_key = config['default']['secret_key']
app.config['JWT_SECRET_KEY'] = app.secret_key
app.config['social_google'] = {
    'client_id': config['social']['google']['client_id'],
    'client_secret': config['social']['google']['client_secret']
}
version = config['version']


print('****************** PRODUCTION MODE ******************')
postgres = config["postgres"]

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(
#                                                 postgres["user"],
#                                                 postgres["pw"],
#                                                 postgres["endpoint"],
#                                                 postgres["port"],
#                                                 postgres["db"])

POSTGRES = {
    'user': 'careertalk',
    'pw': 'careertalk',
    'db': 'careertalk',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(POSTGRES['user'],
                                                                             POSTGRES['pw'],
                                                                             POSTGRES['host'],
                                                                             POSTGRES['port'],
                                                                             POSTGRES['db'])

db = SQLAlchemy(app)
jwt = JWTManager(app)

# build scheduler
sched = BackgroundScheduler()
sched.start()

from careertalk import routes