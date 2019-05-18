import pytest
from flask_sqlalchemy import SQLAlchemy

from careertalk import create_operation
from careertalk.models import CareerFairEmployer, CareerFair, Employer, College
from careertalk_ingest.ingest import CareerFairIngest
from careertalk_load.models import LoadDataIntoPostgres
from common.config import TestIngestConfig, TestLoadConfig


class SQLiteAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        options.update({
            'isolation_level': 'READ UNCOMMITTED',
        })
        super(SQLiteAlchemy, self).apply_driver_hacks(app, info, options)


college = """
INSERT INTO college (name, address, city, zipcode, website, state, uuid)
VALUES ('Some Burrito School', '1200 W Harrison St', 'Chicago', '60607', 'www.uic.edu', 'IL', uuid_generate_v4());
"""

careerfair = """
INSERT INTO careerfair (organization_id, name, date, start_time, end_time, location, address, city, zipcode, uuid)
VALUES (1, 'Burrito', '2019-12-12', '2019-12-12 12:00:00', '2019-12-12 16:00:00', 'Taco', 'Barbeque', 'Chicago', '60608', uuid_generate_v4());
"""


def mock_employers():
    return [['Google', 'FT, INT', 'CS, ES', 'BS, MS, PHD', 'YES'],
            ['Netflix', 'int, Ft', 'ES, CS', 'PhD, bS, Ms', 'No']]


def mock_duplicate_employers():
    return [['Netflix', 'int, Ft', 'ES, CS', 'PhD, bS, Ms', 'No'],
            ['Netflix', 'int, Ft', 'ES, CS', 'PhD, bS, Ms', 'No']]


def mock_urls():
    return ['http://google.com', 'https//www.netflix.com']

def mock_duplicate_urls():
    return ['https//www.netflix.com', 'https//www.netflix.com']


def mock_url_netflix():
    return ['https//www.netflix.com']


@pytest.fixture(scope='module')
def test_ingest_config():
    return TestIngestConfig()


@pytest.fixture(autouse=True)
def _db():
    app, db = create_operation(TestIngestConfig(), "Test")
    with app.app_context():
        db.create_all()
        _init_test_data_load()
        yield db
        db.session.close()
        print("hello")
        db.drop_all()


def _init_test_data_load():
    test_load_config = TestLoadConfig()
    load = LoadDataIntoPostgres(test_load_config)

    print("Initiating Database for Functional Test")
    load.load_schema_using_alchemy()


"""
Test Case:
1. Check if the university is created. Checked
2. Check if the Careerfair is created. Checked
3. Check if a company gets created.    Checked
4. Check if a company gets ingored when it already exists. Impossible in current setting.
5. Check if two companies get created                      Checked
6. Check if only one company gets created when there are two in google sheet.
7. Check if a company gets deleted when it is not coming anymore.
"""


def test_ingest_simple(_db, monkeypatch, test_ingest_config):
    """
    - Test ingest when careerfair and the organization do not exist in our database.
    - Test if ingest utilizes already existing employer information.
    """
    ingest = CareerFairIngest(ingest_config=test_ingest_config)

    monkeypatch.setattr(ingest.gsheet, 'get_employers', mock_employers)
    monkeypatch.setattr(ingest.gsheet, 'get_urls', mock_urls)

    ingest.parse()

    careerfair_employers = CareerFairEmployer.query.all()
    serialized_careerfair_employers = [ce.serialize for ce in careerfair_employers]

    careerfairs = CareerFair.query.all()
    serialized_careerfairs = [c.serialize for c in careerfairs]

    employers = Employer.query.all()
    serialized_employers = [e.serialize for e in employers]

    schools = College.query.all()
    serialized_schools = [s.serialize for s in schools]

    # The first two gets created when we initially load some data. So ignore the first two careerfairs.
    c = serialized_careerfairs[2]
    college = serialized_schools[1]
    google = serialized_careerfair_employers[4]
    netflix = serialized_careerfair_employers[5]

    netflix_employer = Employer.query.filter_by(id=5).first()


    # 4 of them are initially created and 2 of them are created for this test
    assert len(serialized_careerfair_employers) == 6

    # 4 of them are initially created and 1 of them(Netflix) gets created in this test.
    assert len(serialized_employers) == 5

    # 2 of them are initially created and 1 of them gets created in this test.
    assert len(serialized_careerfairs) == 3

    # 1 of them are initially created and 1 of them gets created in this test.
    assert len(serialized_schools) == 2

    assert netflix_employer.company_url == 'netflix.com'

    # assert careerfair
    assert c['name'] == "Burrito"
    assert c['date'] == "12/12/2019"
    assert c['start_time'] == '12:00 PM'
    assert c['end_time'] == '4:00 PM'
    assert c['location'] == 'Taco'
    assert c['address'] == 'Barbeque'
    assert c['city'] == 'Chicago'

    # assert college
    assert college['name'] == "Some Burrito School"

    # assert Employer Netflix
    assert serialized_employers[-1]["name"] == "Netflix"

    # assert CareerFairEmployer Google
    assert google['tables'] == []
    assert google['visa_support'] == 'yes'
    assert google['hiring_majors'] == ['CS', 'ES']
    assert google['hiring_types'] == ['INT', 'FT']
    assert google['degree_requirements'] == ['BS', 'MS', 'PhD']
    assert google['careerfair_id'] == 3

    # assert CareerFairEmployer Netflix
    assert netflix['tables'] == []
    assert netflix['visa_support'] == 'no'
    assert netflix['hiring_majors'] == ['ES', 'CS']
    assert netflix['hiring_types'] == ['INT', 'FT']
    assert netflix['degree_requirements'] == ['BS', 'MS', 'PhD']
    assert netflix['careerfair_id'] == 3

    _db.session.close()


def test_ingest_college_fair_employers_exist(_db, monkeypatch, test_ingest_config):
    """
    - Test ingest when careerfair, organization and the employers already exists.
    - Test if ingest utilizes already existing employer information.
    - Test when there are duplicates in google sheet, create only one.
    """
    global college
    global careerfair

    ingest = CareerFairIngest(ingest_config=test_ingest_config)

    monkeypatch.setattr(ingest.gsheet, 'get_employers', mock_duplicate_employers)
    monkeypatch.setattr(ingest.gsheet, 'get_urls', mock_duplicate_urls)

    ingest.parse()

    careerfair_employers = CareerFairEmployer.query.filter_by(careerfair_id=3).all()

    employers = Employer.query.all()
    print(employers)
    serialized_careerfair_employers = [ce.serialize for ce in careerfair_employers]
    print(serialized_careerfair_employers)

    assert len(serialized_careerfair_employers) == 1

    assert len(employers) == 5
