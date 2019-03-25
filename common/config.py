import json


def _get_config(path):
    with open(path, 'r') as f:
        config = json.load(f)
    return config


class IngestConfig:
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


class GoogleSocialLoginConfig:
    """
    Wrapper class for google social login client credentials.
    """

    def __init__(self):
        google = _get_config("configs/config.json")["social"]["google"]
        self.glogin_client_id = google["client_id"]
        self.glogin_client_secret = google["client_id"]


class Config:

    def __init__(self):
        config = _get_config("configs/config.json")
        self.DEBUG = True
        self.TESTING = False
        self.SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format('careertalk',
                                                                            'careertalk',
                                                                            'localhost',
                                                                            '5432',
                                                                            'careertalk')
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SECRET_KEY = config['secret_key']
        self.ENV = 'development'
        self.JWT_SECRET_KEY = config['secret_key']
        self.VERSION = config['version']
