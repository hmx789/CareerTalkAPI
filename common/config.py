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

        script_base_url = "scripts/"
        self.INSERT_SCRIPT_PATH = script_base_url + "v2_insert_values.sql"
        self.CREATE_SCRIPT_PATH = script_base_url + "v2_create_careerfair.sql"


class TestLoadConfig(LoadConfig):
    def __init__(self):
        LoadConfig.__init__(self)

        self.SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL') or \
                                       'postgresql://{}:{}@{}:{}/{}'.format('careertalk',
                                                                            'careertalk',
                                                                            'localhost',
                                                                            '5432',
                                                                            'careertalk-test')


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


class TestIngestConfig(IngestConfig):

    def __init__(self):
        IngestConfig.__init__(self)
        self.DEBUG = False
        self.TESTING = True

        self.SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL') or \
                                       'postgresql://{}:{}@{}:{}/{}'.format('careertalk',
                                                                            'careertalk',
                                                                            'localhost',
                                                                            '5432',
                                                                            'careertalk-test')


