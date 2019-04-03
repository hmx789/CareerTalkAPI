from common.common_utils import run_script
from sqlalchemy import create_engine


class LoadDataIntoPostgres:
    def __init__(self, config, database):
        engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        self.insert_script_path = config.INSERT_SCRIPT_PATH
        self.create_script_path = config.CREATE_SCRIPT_PATH
        self.conn = engine.connect()
        self.db = database

    def load_schema(self):
        run_script(self.create_script_path, self.conn)
        return True

    # todo: for some reason this one doesn't work T.T
    def load_schema_using_alchemy(self):
        self.db.drop_all()
        self.db.create_all()
        return True

    def insert_values(self):
        run_script(self.insert_script_path, self.conn)
