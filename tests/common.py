import pytest
import jwt
from careertalk import create_rest
from careertalk.models import db
from careertalk_load.models import LoadDataIntoPostgres
from common.config import TestRestConfig, TestLoadConfig


def _init_test_data_load():
    test_load_config = TestLoadConfig()
    load = LoadDataIntoPostgres(test_load_config)
    load.load_schema_using_alchemy()


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_rest(TestRestConfig())

    testing_client = flask_app.test_client()
    testing_client.get()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def _db():
    db.create_all()
    _init_test_data_load()
    yield db
    db.session.close()
    db.drop_all()


def _make_string_jwt_header(user_id):
    payload = {'userId': user_id}
    jwt_header = "Bearer {}".format(jwt.encode(payload, 'super secret key').decode('ASCII'))
    return {'Authorization': jwt_header}


def _send_get_for_private_endpoint(endpoint, test_client, user_id):
    return test_client.get(
        endpoint,
        headers=_make_string_jwt_header(user_id)
    )

def _send_post_for_private_endpoint(endpoint, test_client, user_id):
    return test_client.post(
        endpoint,
        headers=_make_string_jwt_header(user_id)
    )
