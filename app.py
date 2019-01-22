from flask import Flask, redirect, request, make_response
from flask import session as login_session
from flask.json import jsonify
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Fair, Employer, Company, CareerFairEmployers
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
from oauth2client import client, crypt

import json
import httplib2
import requests
import pprint

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
#                                Helper Functions
# ------------------------------------------------------------------------------

def get_user_id(login_session):
    try:
        user = db_session.query(User).filter_by(
                                        email=login_session['email']).one()
        return user.id
    except:
        return None


def create_user(login_session):
    new_user = User(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    db_session.add(new_user)
    db_session.commit()
    user = db_session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_id(login_session):
    try:
        user = db_session.query(User).filter_by(
            email=login_session['email']).one()
        return user.id
    except:
        return None


def is_user_logged_in(login_session):
    if 'username' not in login_session:
        return False
    else:
        return True


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


@app.route('/auth/google/callback', methods=['POST'])
def oauth2callback():
    """Call back for Google Sign-In"""
    CLIENT_ID = config["GOOGLE"]["client_id"]
    # receive the state from the client and compare with the state token in
    # login session
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # get the id_token from the client
    id_token = request.data

    # check issuer if the id token issued by google
    try:
        idinfo = client.verify_id_token(id_token, CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        response = make_response(json.dumps('Invalid token.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = idinfo['sub']
    url = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s' % id_token
    h = httplib2.Http()
    # Get the data from the url.
    data = json.loads(h.request(url, 'GET')[1])

    # Verify that the id token is used for the intended user.
    if data['sub'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the id token is for this app
    if data['aud'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if the user is already logged in.
    stored_id_token = login_session.get('id_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_id_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Save user information to the login session.
    login_session['id_token'] = id_token
    login_session['gplus_id'] = gplus_id
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = get_user_id(login_session)
    # if this user does not existed in the database
    if not user_id:
        user_id = create_user(login_session) # create a user in the database
    login_session['user_id'] = user_id

    result = "Successfully logged in!!!!"
    return result


@app.route('/auth/linkedin/callback', methods=['GET'])
def linkedin_callback():
    linkedin = config["LINKEDIN"]
    linkedin_session = OAuth2Session(linkedin["client_id"],
                                     state=login_session['state'],
                                     redirect_uri=linkedin['redirect_uri'])
    print("fetching token . . . .")
    token = linkedin_session.fetch_token(linkedin["token_url"],
                                         client_secret=linkedin["client_secret"],
                                         code=request.args.get('code'),
                                         authorization_response=request.url)

    login_session['oauth_token'] = token
    return 'linkedin auth success.'


@app.route('/auth/linkedin/entry', methods=['GET'])
def auth_linkedin_entry():
    linkedin = config["LINKEDIN"]
    linkedin_session = OAuth2Session(linkedin["client_id"],
                                     redirect_uri=linkedin["redirect_uri"])

    linkedin_session = linkedin_compliance_fix(linkedin_session)
    authorization_url, state = linkedin_session.authorization_url(
                                                        linkedin['auth_url'])
    login_session["state"] = state
    return redirect(authorization_url)


@app.route('/getlogo', methods=['GET'])
def get_logo():
    l = config["LINKEDIN"]
    with open('linkedin_token.json', 'r') as f:
        linkedin_token = json.load(f)

    linkedin = OAuth2Session(l["client_id"],
                             token=linkedin_token)
    stuff = linkedin.request(
        'get', 'https://api.linkedin.com/v2/organizations?q=vanityName&vanityName=Linkedin')
    return "worked"


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
    companies = db_session.query(CareerFairEmployers).filter(CareerFairEmployers.fair_id == fair_id).all()
    company_list = [company.serialize for company in companies]
    return jsonify(Company=company_list)


if __name__ == "__main__":
    app.secret_key = config['DEFAULT']['SECRET_KEY']
    app.debug = True
    app.run()
