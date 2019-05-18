from careertalk.models import User, Student


def _get_user_by_email(email):
    return User.query.filter_by(personal_email=email).first()


def _get_student_by_user_id(user_id):
    return Student.query.filter_by(user_id=user_id).first()


def _get_student_by_email(email):
    user = User.query.filter_by(personal_email=email).first()
    student = Student.query.filter_by(user_id=user.id).first()

    if user is None:
        raise Exception("This user does not exist: {}".format(email))

    if student is None:
        raise Exception("This student with user email {} does not exist".format(email))

    return student
