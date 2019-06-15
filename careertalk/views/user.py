from flask import Blueprint
from flask import request
from flask.json import jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt

from careertalk.models import db, Student, Like, User
from common.common_utils import _message_builder
from common.getters import _get_student_by_user_id

from sqlalchemy.exc import DataError

user = Blueprint('user', __name__)
session = db.session


def _create_student_user(given_name, family_name, email, profile_img, google_id):
    """
    Create an user and a student account.
    """
    # Create an User
    user = User(
        first_name=given_name,
        last_name=family_name,
        personal_email=email,
        profile_img=profile_img,
        google_id=google_id
    )

    # Store the new user to the database.
    session.add(user)
    # Flush the session to get the user.id
    session.flush()
    # Create a Student
    student = Student(user_id=str(user.id))
    session.add(student)

    session.commit()
    return student


@user.route('/v2/register/student/user', methods=['POST'])
def register_student_user():
    print(request)
    try:
        email = request.headers['email']
        given_name = request.headers['given_name']
        family_name = request.headers['family_name']
        profile_img = request.headers['picture']
        google_id = request.headers['google_id']
        job = request.headers['job'] # currently not used.
    except KeyError as err:
        return _message_builder('Missing headers. {}'.format(err), 400)

    user = User.query.filter_by(google_id=google_id).first()
    if user:
        print("This user already exists")
        return jsonify(user=user.serialize)

    print("creating user ")
    # TODO: when we have faculty or recruiter login functionality, we need more logic to create each model.
    user = _create_student_user(given_name, family_name, email, profile_img, google_id)
    return jsonify(user=user.serialize)


@user.route('/v2/like/<int:careerfair_id>/<int:employer_id>', methods=['POST'])
@jwt_required
def v2_like_company(careerfair_id, employer_id):
    current_user = get_raw_jwt()
    id = current_user["userId"]
    student = _get_student_by_user_id(id)
    # check if this user already liked the company
    like = Like.query \
        .filter_by(student_id=student.id) \
        .filter_by(employer_id=employer_id) \
        .filter_by(careerfair_id=careerfair_id).first()
    # CASE: already liked the company then delete the like
    if like:
        print("Unlike the employer")
        session.delete(like)
        session.commit()
        return _message_builder('Unlike the employer.', 200)

    # CASE: like company
    new_like = Like(student_id=student.id, employer_id=employer_id, careerfair_id=careerfair_id)
    print("new like created. student_id={}, employer_id={} careerfair_id={}".format(student.id,
                                                                                    employer_id,
                                                                                    careerfair_id))
    session.add(new_like)
    session.commit()
    return _message_builder('Succesfully liked an employer', 200)


@user.route('/get/user', methods=['GET'])
@jwt_required
def get_user():
    current_user = get_raw_jwt()
    user_id = current_user["userId"]
    try:
        user = User.query.filter_by(id=user_id).first()
    # when wrong uuid is used, the database server explodes with type error.
    except DataError:
        print("This user does not exist")
        return _message_builder('User does not exist', 404)
    return jsonify(user=user.serialize)
