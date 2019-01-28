from careertalk import app, db
from careertalk.models import Fair, Company, CareerFair, Employer, CareerFairEmployer, User, Student, College, Connection
from flask.json import jsonify
from flask import request, make_response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from google.oauth2 import id_token
from google.auth.transport import requests
import sys

jwt = JWTManager(app)
db_session = db.session

def _user_login(user, token):
    data = jsonify({
        'message': 'Returning User',
        'user': user.serialize,

    })
    response = make_response(data, 200)
    response.headers['UserToken'] = token

    return response


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
    companies = Company.query.filter_by(id=fair_id).all()
    # companies = db_session.query(Company).filter(Company.fair_id == fair_id).all()
    company_list = [company.serialize for company in companies]
    return jsonify(Company=company_list)


@app.route('/careerfairs')
def get_careerfairs():
    fairs = Fair.query.all()
    # fairs = db_session.query(Fair).all()
    fair_list = [fair.serialize for fair in fairs]
    return jsonify(Careerfair=fair_list)


# ------------------------------------------------------------------------------
#                                V2 Endpoints
# ------------------------------------------------------------------------------

@app.route('/v2/careerfairs')
def v2_get_careerfairs():
    fairs = CareerFair.query.all()
    fair_list = [fair.serialize for fair in fairs]
    return_obj = {
        "fairs": fair_list,
        "num_of_fairs": len(fair_list)
    }
    return jsonify(return_obj)


@app.route('/v2/<int:fair_id>/employers', methods=['GET'])
def v2_get_companies(fair_id):
    companies = CareerFairEmployer.filter_by(id=fair_id).all()
    company_list = [company.serialize for company in companies]
    fair = CareerFair.filter_by(id == fair_id).first()
    return jsonify(companies=company_list, num_of_companies=len(company_list), fair=fair.serialize)


# todo
@app.route('/v2/social_login/facebook')
def facbook_login():
    pass

@app.route('/getToken')
def auth():

    token = request.headers['Authorization']
    print(token)
    payload = token.decode(jwt=token, key=app.secret_key)
    return make_response('it worked!', 400)


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/glogin', methods=['POST'])
def google_signup():
    # Check if the request has Authorization header
    if not request.is_json:
        return make_response(jsonify({"msg": "Missing JSON in request"}), 400)
    try:
        token = request.headers['Authorization']
    except KeyError as err:
        print('The Authorization header is not included: ', err)
        response = make_response(jsonify({'message': 'Wrong request'}), 401)
        return response
    # Validate id token.
    try:
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), app.config['social_google']['client_id'])
    except ValueError as err:
        print('The token is not valid: ', sys.exc_info()[1])
        response = make_response(jsonify({'message': 'Wrong token'}), 401)
        return response
    except:
        print("Unexpected error:", sys.exc_info()[1])
        response = make_response(jsonify({'message': 'Unexpected error'}), 401)
        return response

    if id_info['iss'] not in ['https://accounts.google.com', 'accounts.google.com']:
        print("Wrong issuer: ", sys.exc_info()[1])
        response = make_response(jsonify({'message': 'Wrong issuer'}), 401)
        return response

    if id_info['aud'] != app.config['social_google']['client_id']:
        print("Token's aud id does not match app's.", sys.exc_info()[1])
        response = make_response(jsonify({'message': 'Aud does not match.'}), 401)
        return response

    # check if this person already exists in the database.
    check_user = User.query.filter_by(personal_email=id_info['email']).first()
    if check_user:
        # User exists on db. Then just return the existing token to the user.
        connection = Connection.query.filter_by(user_id=check_user.id).first()
        user_token = connection.token
        return _user_login(check_user, user_token)

    userid = id_info['sub']
    username = id_info['name']
    given_name = id_info['given_name']
    family_name = id_info['family_name']
    email = id_info['email']
    profile_img = id_info['picture']

    # Create an User
    user = User(first_name=given_name, last_name=family_name, personal_email=email, profile_img=profile_img)
    # Store the new user to the database.
    db_session.add(user)
    # Flush the session to get the user.id
    db_session.flush()
    # Create a Student
    student = Student(user_id=user.id)

    # generate access token based on the identity
    identity = {'email': email, 'username': username, 'pub_userid': userid}
    access_token = create_access_token(identity=identity)
    # Create a Connection
    connection = Connection(user_id=user.id, public_id=userid, token=access_token)

    db_session.add(student)
    db_session.add(connection)
    db_session.commit()

    return _user_login(user, access_token)

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

