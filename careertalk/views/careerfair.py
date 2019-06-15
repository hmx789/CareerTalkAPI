from flask import make_response, render_template, Blueprint
from flask.json import jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt

from careertalk.models import (
    Fair, Company, CareerFair, CareerFairEmployer, Student, Like, Top5
)
from common.getters import _get_student_by_user_id

careerfair = Blueprint('careerfair', __name__)


def _get_student(user):
    student = Student.query.filter_by(user_id=user["user_id"]).first()
    return student

# ------------------------------------------------------------------------------
#                                Routes
# ------------------------------------------------------------------------------


@careerfair.route('/')
@careerfair.route('/views')
def main():
    return "hello world"


@careerfair.route('/careertalk/support')
def support_info():
    return render_template('contact.html')


@careerfair.route('/careertalk/private_policy')
def private_policy():
    return render_template('private_policy.html')


# ------------------------------------------------------------------------------
#                                V1 Endpoints
# ------------------------------------------------------------------------------


@careerfair.route("/<int:fair_id>/companies", methods=['GET'])
def get_companies(fair_id):
    companies = Company.query.filter_by(fair_id=fair_id).all()
    company_list = [company.serialize for company in companies]
    return jsonify(Company=company_list)


@careerfair.route('/careerfairs')
def get_careerfairs():
    fairs = Fair.query.all()
    fair_list = [fair.serialize for fair in fairs]
    return jsonify(Careerfair=fair_list)


# ------------------------------------------------------------------------------
#                                V2 Endpoints
# ------------------------------------------------------------------------------

@careerfair.route('/v2/careerfairs')
def v2_get_careerfairs():
    fairs = CareerFair.query.all()

    print(fairs)
    fair_list = [fair.serialize for fair in fairs]
    return_obj = {
        "fairs": fair_list,
        "num_of_fairs": len(fair_list)
    }
    return jsonify(return_obj)


@careerfair.route('/v2/<string:fair_id>/anon_user/employers', methods=['GET'])
def v2_get_companies_anonuser(fair_id):
    companies = CareerFairEmployer.query.filter_by(careerfair_id=fair_id).all()
    company_list = [company.serialize for company in companies]
    fair = CareerFair.query.filter_by(id=fair_id).first().serialize
    return jsonify(companies=company_list, num_of_companies=len(company_list), fair=fair)


@careerfair.route('/v2/<string:fair_id>/employers', methods=['GET'])
@jwt_required
def v2_get_companies(fair_id):
    current_user = get_raw_jwt()
    user_id = current_user["userId"]

    student = _get_student_by_user_id(user_id)
    if not student:
        return make_response("This user is not student.")
    companies = CareerFairEmployer.query.filter_by(careerfair_id=fair_id).all()

    # Get liked company and make them as a set
    liked_companies = Like.query.filter_by(student_id=str(student.id)).filter_by(careerfair_id=str(fair_id)).all()
    liked_company_ids = set()

    # Iterate over the liked_companies list and put id into the set.
    for liked_company in liked_companies:
        liked_company_ids.add(liked_company.employer_id)

    # list to return the company list.
    company_list = []

    # iterate over the companies and add 'is_liked' key val pair if user liked the company.
    for company in companies:
        c = company.serialize
        c["is_liked"] = True if c["employer"]["id"] in liked_company_ids else False
        company_list.append(c)

    fair = CareerFair.query.filter_by(id=fair_id).first()
    if not fair:
        return make_response("This careerfair does not exist", 404)

    return jsonify(companies=company_list, num_of_companies=len(company_list), fair=fair.serialize)


@careerfair.route('/v2/<string:careerfair_id>/top5', methods=['GET'])
@jwt_required
def top5_company(careerfair_id):
    top = Top5.query.filter_by(careerfair_id=careerfair_id).first()
    return jsonify(top.serialize)


@careerfair.route('/careertalk/version', methods=['GET'])
def version_check():
    return jsonify({'version': "2.0.1"})
