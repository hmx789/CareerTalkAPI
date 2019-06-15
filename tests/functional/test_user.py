import jwt
import pytest

from careertalk import create_rest
from careertalk.models import db, User
from careertalk_load.models import LoadDataIntoPostgres
from common.config import TestRestConfig, TestLoadConfig



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

"""
def _db():
    app, db = create_operation(TestIngestConfig(), "Test")
    with app.app_context():
        db.create_all()
        _init_test_data_load()
        yield db
        db.session.close()
        db.drop_all()
        
        """

# TODO: Tech dept this database and _init_test_data_load should be moved to the library.
@pytest.fixture(scope='module')
def _db():
    db.create_all()
    _init_test_data_load()
    yield db
    db.session.close()
    db.drop_all()


def _init_test_data_load():
    test_load_config = TestLoadConfig()
    load = LoadDataIntoPostgres(test_load_config)

    print("Initiating Database for Functional Test")
    load.load_schema_using_alchemy()


@pytest.fixture(scope='module')
def new_user():
    user = User(
        google_id="burrito",
        first_name="taco",
        last_name="bell",
        middle_name="coke",
        personal_email="test@gmail.com",
        profile_img="someurl"
    )
    return user


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the attributes
    """
    assert new_user.personal_email == "test@gmail.com"
    assert new_user.google_id == "burrito"
    assert new_user.first_name == "taco"
    assert new_user.last_name == "bell"
    assert new_user.middle_name == "coke"
    assert new_user.profile_img == "someurl"


def test_register_user_student(test_client, _db):
    """
    GIVEN a HTTP POST request
    WHEN with proper headers
    THEN create a user and a student.
    """

    # CASE: missing email
    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'given_name': 'pikachu',
                                    'family_name': 'detective',
                                    'picture': 'pikachu picture',
                                    'google_id': 'some google id',
                                    'job': 'student'
                                })

    assert response.status_code == 400

    # CASE: missing given name
    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'family_name': 'detective',
                                    'picture': 'pikachu picture',
                                    'google_id': 'some google id',
                                    'job': 'student'
                                })

    assert response.status_code == 400

    # CASE: missing family name
    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'given_name': 'pikachu',
                                    'picture': 'pikachu picture',
                                    'google_id': 'some google id',
                                    'job': 'student'
                                })

    assert response.status_code == 400

    # CASE: missing profile image
    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'given_name': 'pikachu',
                                    'family_name': 'detective',
                                    'google_id': 'some google id',
                                    'job': 'student'
                                })

    assert response.status_code == 400

    # CASE: missing google_id
    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'given_name': 'pikachu',
                                    'family_name': 'detective',
                                    'picture': 'pikachu picture',
                                    'job': 'student'
                                })

    assert response.status_code == 400

    # CASE: missing job
    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'given_name': 'pikachu',
                                    'family_name': 'detective',
                                    'picture': 'pikachu picture',
                                    'google_id': 'some google id'
                                })

    assert response.status_code == 400

    # CASE: success
    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'given_name': 'pikachu',
                                    'family_name': 'detective',
                                    'picture': 'pikachu picture',
                                    'google_id': 'some google id',
                                    'job': 'student'
                                })

    assert response.status_code == 200


def _make_user_response_with_id(test_client, user_id):
    USER_ENDPOINT = '/get/user'
    payload = {'userId': user_id}
    jwt_str = 'Bearer ' + jwt.encode(payload, 'super secret key').decode('ASCII')
    return test_client.get(USER_ENDPOINT, headers={'Authorization': jwt_str})


def test_get_user(test_client, _db):
    existing_test_user = User.query.filter_by(first_name='Seho').first()
    response = _make_user_response_with_id(test_client, str(existing_test_user.id))
    user_response_json = response.get_json()

    assert response.status_code == 200
    assert user_response_json['user']['first_name'] == 'Seho'
    assert user_response_json['user']['google_id'] is None
    assert user_response_json['user']['last_name'] == 'Lim'
    assert user_response_json['user']['middle_name'] is None
    assert user_response_json['user']['personal_email'] == 'seho@gmail.com'
    assert user_response_json['user']['profile_url'] == 'default_profile.png'

    # CASE: Test with weird jwt
    response = test_client.get('/get/user', headers={'Authorization': 'weird string'})
    # HTTP 422: UNPROCESSABLE ENTITY
    assert response.status_code == 422

    # CASE: wrong UUID
    response = _make_user_response_with_id(test_client, 'some weird id')
    assert response.status_code == 404
    assert b'User does not exist' in response.data
