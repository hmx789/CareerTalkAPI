from flask import Flask
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Company, Fair

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

app = Flask(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

postgres = config["POSTGRES"]
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
                                                postgres["user"],
                                                postgres["pw"],
                                                postgres["endpoint"],
                                                postgres["port"],
                                                postgres["db"]))

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

def get_company_info():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    SPREADSHEET_ID = '1fKG4iVnj9coxg2mwip4reD7Rt5eiBvlEDM-Hu84M3zE'
    RANGE_NAME = 'Sheet1!A4:E48'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('gsheet_credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    values = result.get('values', [])

    return values


def insert_rows():
    """
    :return:
    """
    data = get_company_info()

    for row in data:
        name = row[0]

        if row[1].strip().lower() == 'int':
            type = 1
        elif row[1].strip().lower() == 'ft':
            type = 2
        else :
            type = 3

        if row[3].strip().lower() == 'bs':
            degree = 1
        elif row[3].strip().lower() == 'ms':
            degree = 2
        elif row[3].strip().lower() == 'phd':
            degree = 3
        elif row[3].strip().lower() == 'bs, ms':
            degree = 4
        elif row[3].strip().lower() == 'bs, phd':
            degree = 5
        elif row[3].strip().lower() == 'ms, phd':
            degree = 6
        else:
            degree = 8

        if row[4].strip().lower() == 'yes':
            visa = 1
        elif row[4].strip().lower() == 'no':
            visa = 2
        else:
            vias = 3

        print("name: {}, hiringtype: {}, degree: {}, visa: {}".format(name,
                                                                      type,
                                                                      degree,
                                                                      visa))
        print(row[2])
        print("Adding a company . . .")

        company = Company(name=name, hiring_types=type, hiring_majors=row[2],
                          degree=degree, visa=visa, fair_id=1)
        session.add(company)
        session.commit()


@app.route('/')
@app.route('/main')
def main():
    return "hello world"

if __name__ == "__main__":
    app.secret_key = config['DEFAULT']['SECRET_KEY']
    app.debug = True
    app.run()
