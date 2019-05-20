import pytest
from careertalk.models import db, User
from careertalk import create_rest
from common.config import TestRestConfig


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
    yield db
    db.session.close()
    db.drop_all()


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


def test_register_user_student(test_client):
    """
    GIVEN a HTTP POST request
    WHEN with proper headers
    THEN create a user and a student.
    """

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



def test_register_user_student(test_client):
    """
    GIVEN a HTTP POST request
    WHEN with proper headers
    THEN create a user and a student.
    """
    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'given_name': 'pikachu',
                                    'family_name': 'detective',
                                    'picture': 'pikachu picture',
                                    'google_id': 'some google id',
                                    'job': 'student'
                                })

    assert response.status_code == 400

    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'family_name': 'detective',
                                    'picture': 'pikachu picture',
                                    'google_id': 'some google id',
                                    'job': 'student'
                                })

    assert response.status_code == 400

    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'given_name': 'pikachu',
                                    'picture': 'pikachu picture',
                                    'google_id': 'some google id',
                                    'job': 'student'
                                })

    assert response.status_code == 400

    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'given_name': 'pikachu',
                                    'family_name': 'detective',
                                    'google_id': 'some google id',
                                    'job': 'student'
                                })

    assert response.status_code == 400

    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'given_name': 'pikachu',
                                    'family_name': 'detective',
                                    'picture': 'pikachu picture',
                                    'job': 'student'
                                })

    assert response.status_code == 400

    response = test_client.post('/v2/register/student/user',
                                headers={
                                    'email': 'seho@gmail.com',
                                    'given_name': 'pikachu',
                                    'family_name': 'detective',
                                    'picture': 'pikachu picture',
                                    'google_id': 'some google id'
                                })

    assert response.status_code == 400
