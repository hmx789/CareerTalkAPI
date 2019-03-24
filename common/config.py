import json


def _get_config(path):
    with open(path, 'r') as f:
        config = json.load(f)
    return config


class IngestConfig():
    """
    Wrapper class for ingest configs. Currently this config only load a single ingest
    job.

    TODO: This class will be loading the actual credentials from safe database.
    """

    def __init__(self):
        config = _get_config("configs/ingest-config.json")["gsheet"]
        # TODO: later one this should be just base location of all the jobs.
        self.work_path = "careertalk_ingest/ingest_jobs/uic-02132019-engineering-fair.json"
        self.token_path = config["token_path"]
        self.cred_path = config["cred_path"]
        self.scope = config["scope"]
        self.discovery_version = config["discovery_version"]
        self.service = config["service"]


class Config():
    postgres = {
        'user': 'careertalk',
        'pw': 'careertalk',
        'db': 'careertalk',
        'host': 'localhost',
        'port': '5432',
    }
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format('careertalk',
                                                                   'careertalk',
                                                                   'localhost',
                                                                   '5432',
                                                                   'careertalk')


class ProductionConfig(Config):
    DATABASE_URI = 'todo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
