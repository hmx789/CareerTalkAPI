from careertalk.models import User, Student
from sqlalchemy.exc import DataError


def _get_user_by_email(email):
    try:
        return User.query.filter_by(personal_email=email).first()
    except DataError:
        return None


def _get_student_by_user_id(user_id):
    try:
        return Student.query.filter_by(user_id=user_id).first()
    except DataError:
        return None
