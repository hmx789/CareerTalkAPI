from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

app = Flask(__name__)
db = SQLAlchemy(app)

with open('config.json', 'r') as f:
    config = json.load(f)

Base = declarative_base()

if app.debug:
    app.config['SQLALCHEMY_DATABASE_URI'] = config['default']['local_db']
    engine = create_engine('sqlite:///careertalk.db',
                            connect_args={'check_same_thread': False},
                            echo=False)

else:
    postgres = config["postgres"]
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(
                                                    postgres["user"],
                                                    postgres["pw"],
                                                    postgres["endpoint"],
                                                    postgres["port"],
                                                    postgres["db"])

from careertalk import routes