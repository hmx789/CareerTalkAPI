from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable

from common.common_utils import run_script


# This patches some native sqlalchemy functions to add CASCADE on the query when dropping tables.
@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


class LoadDataIntoPostgres:
    def __init__(self, config, app, db):
        engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        self.load_config = config
        self.insert_script_path = config.INSERT_SCRIPT_PATH
        self.create_script_path = config.CREATE_SCRIPT_PATH
        self.conn = engine.connect()
        self.app = app
        self.db = db

    def load_schema_using_alchemy(self):
        print("Start Data Loading Using Alchemy.")
        print("WARNING: This operation drop all existing tables and create tables.")

        with self.app.app_context():
            self.db.drop_all()
            print("SUCCESS: DROPPED all the existing tables")
            self.db.create_all()
            print("SUCCESS: CREATED all the existing tables")
            self._insert_seed_values()
            print("SUCCESS: RAN all the seeding sql queries")

        print("SUCCESS: Successfully Loaded All Data on {}".format(self.app.config['SQLALCHEMY_DATABASE_URI']))
        self.db.session.close()
        return True

    # WARNING: This might not work very well if the sql scripts are not up to date!!
    def load_data_using_script(self):
        print("Data Load: Use sql scripts.")
        print("Warning: This might create issues if sql scripts are not up to date. ")
        self._load_schema()
        self._insert_seed_values()

    def _load_schema(self):
        run_script(self.create_script_path, self.conn)
        return True

    def _insert_seed_values(self):
        run_script(self.insert_script_path, self.conn)
