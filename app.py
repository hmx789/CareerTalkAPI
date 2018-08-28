from flask import Flask, redirect, request
from flask import session as login_session
from flask.json import jsonify
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Company, Fair
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

import json
import requests
import pprint

app = Flask(__name__)
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

with open('config.json', 'r') as f:
    config = json.load(f)

postgres = config["POSTGRES"]
"""
use this one on production

engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
                                                postgres["user"],
                                                postgres["pw"],
                                                postgres["endpoint"],
                                                postgres["port"],
                                                postgres["db"]))
"""

engine = create_engine('sqlite:///careertalk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()




@app.route('/')
@app.route('/main')
def main():
    return "hello world"


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
    print(token)
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
    print("Redirect User!!!")
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
    print(stuff)

    return "worked"


# insert_rows()
if __name__ == "__main__":
    app.secret_key = config['DEFAULT']['SECRET_KEY']
    app.debug = True
    app.run(ssl_context='adhoc')
