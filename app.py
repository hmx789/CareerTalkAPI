from flask import Flask, redirect, request, make_response
from flask import session as login_session
from flask.json import jsonify
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Fair, Employer, Company, CareerFairEmployer
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
from oauth2client import client, crypt
import json
import httplib2

app = Flask(__name__)
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

with open('config.json', 'r') as f:
    config = json.load(f)

postgres = config["POSTGRES"]
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
                                                postgres["user"],
                                                postgres["pw"],
                                                postgres["endpoint"],
                                                postgres["port"],
                                                postgres["db"]))

# engine = create_engine('sqlite:///careertalk.db',
#                         connect_args={'check_same_thread': False},
#                         echo=False)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

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
    return jsonify(Company=company_list)


if __name__ == "__main__":
    app.secret_key = config['DEFAULT']['SECRET_KEY']
    app.debug = True
    app.run()
