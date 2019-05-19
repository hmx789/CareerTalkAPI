from careertalk.models import User, Student


def _get_user_by_email(email):
    return User.query.filter_by(personal_email=email).first()


def _get_student_by_user_id(user_id):
    return Student.query.filter_by(user_id=user_id).first()
