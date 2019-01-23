from careertalk import app
from careertalk import db_session
from careertalk.models import Fair, Company, CareerFairEmployer
from flask.json import jsonify

# ------------------------------------------------------------------------------
#                                Routes
# ------------------------------------------------------------------------------


@app.route('/')
@app.route('/main')
def main():
    return "hello world"


@app.route('/careertalk/support')
def support_info():
    html =  '''
    <!DOCTYPE html>
        <html>
            <body>
                <h1>CareerTalk Support</h1>
                <p>Name: Seho Lim</p>
                <p>Email: limseho657424@gmail.com </p>
            </body>
        </html>
    '''
    return html


# ------------------------------------------------------------------------------
#                                V1 Endpoints
# ------------------------------------------------------------------------------

@app.route("/<int:fair_id>/companies", methods=['GET'])
def get_companies(fair_id):
    companies = db_session.query(Company).filter(Company.fair_id == fair_id).all()
    company_list = [company.serialize for company in companies]
    return jsonify(Company=company_list)


@app.route('/careerfairs')
def get_careerfairs():
    fairs = db_session.query(Fair).all()
    fair_list = [fair.serialize for fair in fairs]
    return jsonify(Careerfair=fair_list)


# ------------------------------------------------------------------------------
#                                V2 Endpoints
# ------------------------------------------------------------------------------

@app.route('/v2/careerfairs')
def v2_get_careerfairs():
    fairs = db_session.query(Fair).all()
    fair_list = [fair.serialize for fair in fairs]
    return_obj = {
        "fairs": fair_list,
        "num_of_fairs": len(fair_list)
    }
    return jsonify(return_obj)


@app.route('/v2/<int:fair_id>/employers', methods=['GET'])
def v2_get_companies(fair_id):
    companies = db_session.query(CareerFairEmployer).filter(CareerFairEmployer.fair_id == fair_id).all()
    company_list = [company.serialize for company in companies]
    fair = db_session.query(Fair).filter(Fair.id == fair_id).one()
    return jsonify(companies=company_list, num_of_companies=len(company_list), fair=fair.serialize)


# todo
@app.route('/v2/facebook')
def facbook_login(token):
    pass