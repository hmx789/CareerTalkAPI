import json
import os

env = os.environ
test_database = 'postgresql://{}:{}@{}:{}/{}'.format('careertalk',
                                                     'careertalk',
                                                     'localhost',
                                                     '5432',
                                                     'careertalk-test')

local_database = 'postgresql://{}:{}@{}:{}/{}'.format('careertalk',
                                                      'careertalk',
                                                      'localhost',
                                                      '5432',
                                                      'careertalk')

def _get_config(path):
    with open(path, 'r') as f:
        config = json.load(f)
    return config


class Config:
    DEBUG = env.get("DEBUG") or True
    TESTING = env.get("TESTING") or False
    ENV = env.get("ENV") or "development"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = env.get('SECRET_KEY') or "super secret key"
    SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL') or local_database



class CareerTalkConfig(Config):

    def __init__(self):
        Config.__init__(self)
        self.VERSION = "2.0.1"


class LoadConfig(Config):

    def __init__(self):
        Config.__init__(self)

        self.insert_script_path = "scripts/v2_insert_values.sql"
        self.create_script_path = "scripts/v2_create_careerfair.sql"


class IngestConfig(Config):
    """
    Wrapper class for ingest configs. Currently this config only load a single ingest
    job.
    """
    def __init__(self):
        Config.__init__(self)
        # TODO: later one this should be just base location of all the jobs.
        if self.DEBUG == "True":
            self.credentials = _get_config("configs/ingest-credentials.json")
        else:
            self.credentials = {
                "installed": {
                    "client_id": env.get("GSHEET_CLIENT_ID"),
                    "client_secret": env.get("GSHEET_CLIENT_SECRET"),
                    "project_id": env.get("GSHEET_CLIENT_SECRET"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                }
            }

        self.work_path = "careertalk_ingest/ingest_jobs/uic-02132019-engineering-fair.json"
        self.token_path = "configs/gsheet-token.json"
        self.scope = "https://www.googleapis.com/auth/spreadsheets.readonly"
        self.discovery_version = "v4"
        self.service = "sheets"
        self.sheet_link_field = "sheets/data/rowData/values/hyperlink"


class TestIngestConfig():
    DEBUG = False
    Testing = True
    ENV = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    work_path = 'tests/resources/ingest-job-test.json'
    SQLALCHEMY_DATABASE_URI = test_database
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
    SQLALCHEMY_DATABASE_URI = test_database
