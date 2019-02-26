from careertalk import db, app
from sqlalchemy.sql import text
from sqlalchemy import create_engine

from configs.constants import LOAD_CONFIG

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
con = engine.connect()

class LoadDataIntoPostgres:
    def __init__(self, load_config, database, connection):
        self.load_config_path = load_config
        self.db = database
        self.conn = connection
    def load_schema(self):
        self.db.create_all()
        return True
    def insert_values(self):
        s = text("INSERT INTO hiring_type (type) VALUES ('FT')")
        result = self.conn.execute(s)
        print(result)


load = LoadDataIntoPostgres(LOAD_CONFIG, db, con)


