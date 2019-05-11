import json
import os

env = os.environ

def _get_config(path):
    with open(path, 'r') as f:
        config = json.load(f)
    return config


class Config:
    DEBUG = True
    TESTING = False
    ENV = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):

        self.config = _get_config("configs/config.json")
        self.SECRET_KEY = env.get('SECRET_KEY') or self.config['secret_key']
        self.SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL') or \
                                       'postgresql://{}:{}@{}:{}/{}'.format('careertalk',
                                                                            'careertalk',
                                                                            'localhost',
                                                                            '5432',
                                                                            'careertalk')


class CareerTalkConfig(Config):

    def __init__(self):
        Config.__init__(self)

        config = self.config
        self.VERSION = config['version']


class LoadConfig(Config):

    def __init__(self):
        Config.__init__(self)

        self.insert_script_path = "scripts/v2_insert_values.sql"
        self.create_script_path = "scripts/v2_create_careerfair.sql"


class IngestConfig(Config):
    """
    Wrapper class for ingest configs. Currently this config only load a single ingest
    job.

    TODO: This class will be loading the actual credentials from safe database.
    """

    def __init__(self):
        Config.__init__(self)

        config = _get_config("configs/ingest-config.json")["gsheet"]
        # TODO: later one this should be just base location of all the jobs.
        self.work_path = "careertalk_ingest/ingest_jobs/uic-02132019-engineering-fair.json"
        self.token_path = config["token_path"]
        self.cred_path = config["cred_path"]
        self.scope = config["scope"]
        self.discovery_version = config["discovery_version"]
        self.service = config["service"]


class TestIngestConfig():
    DEBUG = False
    Testing = True
    ENV = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    work_path = 'tests/resources/ingest-job-test.json'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format('careertalk',
                                                                    'careertalk',
                                                                    'localhost',
                                                                    '5432',
                                                                    'careertalk-test')
    service = "sheets"
    discovery_version = "v4"
    scope = "https://www.googleapis.com/auth/spreadsheets.readonly"
    token_path = "configs/gsheet-token.json"
    cred_path = "configs/ingest-credentials.json"


class TestLoadConfig():
    DEBUG = False
    Testing = True
    ENV = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    insert_script_path = "scripts/v2_insert_values.sql"
    create_script_path = "scripts/v2_create_careerfair.sql"
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format('careertalk',
                                                                    'careertalk',
                                                                    'localhost',
                                                                    '5432',
                                                                    'careertalk-test')
