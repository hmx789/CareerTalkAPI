from flask import Blueprint
from flask import request

from careertalk.models import db, User, Student, Like
from common.common_utils import _message_builder, _check_identity_header
from common.getters import _get_student_by_user_id

user = Blueprint('user', __name__)
session = db.session


def _create_student_user(given_name, family_name, email, profile_img, google_id):
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
    student = Student(user_id=user.id)
    session.add(student)

    session.commit()
    return student


# headers: { googleId, email, given_name, family_name, picture },
@user.route('/v2/register/student/user', methods=['POST'])
def register_student_user():
    try:
        email = request.headers['email']
        given_name = request.headers['given_name']
        family_name = request.headers['family_name']
        profile_img = request.headers['picture']
        google_id = request.headers['google_id']
    except KeyError as err:
        return _message_builder('Missing values in the header. {}'.format(err), 400)

    user = _get_student_by_user_id(id)

    # todo: when we have faculty or recruiter login functionality
    #      we need more logic to create each model.

    # Check if the user already exists
    if user is None:
        _create_student_user(given_name, family_name, email, profile_img, google_id)
        return _message_builder("Successfully registered a student : {}".format(email), 200)

    return _message_builder("This student user already exists", 200)


@user.route('/v2/like/<int:careerfair_id>/<int:employer_id>', methods=['POST'])
def v2_like_company(careerfair_id, employer_id):
    id = _check_identity_header(request.headers, "id")
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
