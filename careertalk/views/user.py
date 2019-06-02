from flask import Blueprint
from flask import request
from flask.json import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from careertalk.models import db, Student, Like, User
from common.common_utils import _message_builder, _check_identity_header
from common.getters import _get_student_by_user_id

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
    try:
        email = request.headers['email']
        given_name = request.headers['given_name']
        family_name = request.headers['family_name']
        profile_img = request.headers['picture']
        google_id = request.headers['google_id']
        job = request.headers['job']
    except KeyError as err:
        return _message_builder('Missing headers. {}'.format(err), 400)


    user = User.query.filter_by(google_id=google_id).first()
    if user:
        return jsonify(user=user.serialize)

    # todo: when we have faculty or recruiter login functionality
    #      we need more logic to create each model.
    user = _create_student_user(given_name, family_name, email, profile_img, google_id)
    return jsonify(user=user.serialize)


@user.route('/v2/like/<int:careerfair_id>/<int:employer_id>', methods=['POST'])
@jwt_required
def v2_like_company(careerfair_id, employer_id):
    current_user = get_jwt_identity()
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


@user.route('/user/<string:id>')
def get_user(id):
    pass
