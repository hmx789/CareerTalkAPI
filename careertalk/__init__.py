from flask import Flask
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json


app = Flask(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

Base = declarative_base()
postgres = config["POSTGRES"]
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
                                                postgres["user"],
                                                postgres["pw"],
                                                postgres["endpoint"],
                                                postgres["port"],
                                                postgres["db"]))

# engine = create_engine('sqlite:///careertalk.db',
#                         connect_args={'check_same_thread': False},
#                         echo=False)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

from careertalk import routes