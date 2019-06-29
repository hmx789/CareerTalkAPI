import pytest

from careertalk.models import User, CareerFair, Employer, Like, Student
from tests.common import _init_test_data_load, test_client, _db, _send_post_for_private_endpoint, \
    _send_get_for_private_endpoint

print(_init_test_data_load)
print(test_client)
print(_db)


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


def test_get_user(test_client, _db):
    ENDPOINT = '/get/user'
    existing_test_user = User.query.filter_by(first_name='Seho').first()
    response = _send_get_for_private_endpoint(ENDPOINT, test_client, str(existing_test_user.id))
    json = response.get_json()
    assert response.status_code == 200
    assert json['first_name'] == 'Seho'
    assert json['google_id'] is None
    assert json['last_name'] == 'Lim'
    assert json['middle_name'] is None
    assert json['personal_email'] == 'seho@gmail.com'
    assert json['profile_url'] == 'default_profile.png'


    # CASE: Test with weird jwt
    response = test_client.get('/get/user', headers={'Authorization': 'weird string'})
    # HTTP 422: UNPROCESSABLE ENTITY
    assert response.status_code == 422
    # CASE: wrong UUID

    response = _send_get_for_private_endpoint(ENDPOINT, test_client, 'some weird id')
    assert response.status_code == 400
    assert b'Bad request' in response.data


def test_v2_like_company(test_client, _db):
    careerfair = CareerFair.query.filter_by(name='test careerfair').first()
    careerfair_id = str(careerfair.id)
    employer = Employer.query.filter_by(name='Google').first()
    employer_id = str(employer.id)
    existing_test_user_id = str(User.query.filter_by(first_name='Seho').first().id)
    seho_student_id = str(Student.query.filter_by(user_id=existing_test_user_id).first().id)
    ENDPOINT = '/v2/like/{}/{}'.format(careerfair_id, employer_id)

    # CASE: like an employee
    response = _send_post_for_private_endpoint(ENDPOINT, test_client, existing_test_user_id)
    assert response.status_code == 200

    like = Like.query.filter_by(employer_id=employer_id, careerfair_id=careerfair_id, student_id=seho_student_id).first()

    assert like.careerfair_id == careerfair_id
    assert like.employer_id == employer_id
    assert like.student_id == seho_student_id

    # CASE: dis like the employee (toggle)
    response = _send_post_for_private_endpoint(ENDPOINT, test_client, existing_test_user_id)
    assert response.status_code == 200

    like = Like.query.filter_by(employer_id=employer_id, careerfair_id=careerfair_id, student_id=seho_student_id).first()
    assert like == None


