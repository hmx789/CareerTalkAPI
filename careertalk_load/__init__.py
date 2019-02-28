from careertalk import db, app
from sqlalchemy import create_engine
from common.common_utils import run_script

from configs.constants import LOAD_CONFIG
import json

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
con = engine.connect()


class LoadDataIntoPostgres:
    def __init__(self, load_config, database, connection):
        with open(load_config, 'r') as f:
            config = json.load(f)
            self.load_config_path = config["insert_query_path"]

        self.db = database
        self.conn = connection

    def load_schema(self):
        self.db.drop_all()
        self.db.create_all()
        return True

    def insert_values(self):
        print(self.load_config_path)
        run_script(self.load_config_path, self.conn)


load = LoadDataIntoPostgres(LOAD_CONFIG, db, con)
