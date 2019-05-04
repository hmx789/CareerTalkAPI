import pytest
import mock
import pytest
from pytest_mock import mocker

from careertalk_ingest.ingest import CareerFairIngest
from careertalk import create_operation
from careertalk.models import CareerFairEmployer
from careertalk_load.models import LoadDataIntoPostgres
from common.config import TestIngestConfig, TestLoadConfig


app, db = create_operation(TestIngestConfig(), "Test Ingest")


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    print(db)
    print(app)
    with app.app_context():
        db.create_all()
        _init_test_data_load()
        yield db  # this is where the testing happens!

        db.session.close()

        db.drop_all()


def _init_test_data_load():
    test_load_config = TestLoadConfig()
    app, db = create_operation(TestLoadConfig(), "test")
    load = LoadDataIntoPostgres(test_load_config, app, db)

    print("Initiating Database for Functional Test")
    load.load_schema_using_alchemy()


def test_ingest(init_database, monkeypatch):
    print("testing ingest")
    test_ingest_config = TestIngestConfig()
    ingest = CareerFairIngest(ingest_config=test_ingest_config, app=app, db=db)

    print("Start Data Ingestion")
    def mock_employers():
        return [['Google', 'FT, INT', 'CS, ES', 'BS, MS, PHD', 'YES']]
    def mock_urls():
        return ['http://google.com']
    monkeypatch.setattr(ingest.gsheet, 'get_employers', mock_employers)
    monkeypatch.setattr(ingest.gsheet, 'get_urls', mock_urls)

    ingest.parse()

    careerfairs = CareerFairEmployer.query.all()
    careerfair_list = [cf.serialize for cf in careerfairs]
    assert len(careerfair_list) == 5

