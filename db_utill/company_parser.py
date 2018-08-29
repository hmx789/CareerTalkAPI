from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
import os, inspect, sys, re
# direct import the database_setup module.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from database_setup import Base, Company


def get_db_connection():
    engine = create_engine('sqlite:///../careertalk.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()
    return db_session


def match_company_url(raw_url, pattern):
    matches = pattern.finditer(raw_url)
    url = ''
    for m in matches:
        url = m.group(2) + m.group(3)
        if 'www.' in m.group(2):
            url = url[4:]
    return url


def get_company_info():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    SPREADSHEET_ID = '1fKG4iVnj9coxg2mwip4reD7Rt5eiBvlEDM-Hu84M3zE'
    RANGE_NAME = 'Sheet1!A4:E48'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('../gsheet_credentials.json',
                                              SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()

    values = result.get('values', [])
    links = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID,
        ranges=RANGE_NAME,
        fields="sheets/data/rowData/values/hyperlink"
    ).execute()
    # print("============================================================")
    # pp = pprint.PrettyPrinter(indent=1)
    # pp.pprint(links)
    # print("============================================================")
    links_rows = links['sheets'][0]['data'][0]['rowData']
    pattern = re.compile('(//)(.+\.)(com|org|net|edu|gov|mil)')
    urls = []
    for val in links_rows:
        raw_url = val['values'][0]['hyperlink']
        url = match_company_url(raw_url, pattern)
        urls.append(url)
        # print(url)
    return values, urls


def insert_rows():
    data, urls = get_company_info()
    for i, row in enumerate(data):
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
            degree = 7
        if row[4].strip().lower() == 'yes':
            visa = 1
        elif row[4].strip().lower() == 'no':
            visa = 2
        else:
            visa = 3

        print(len(data), len(urls))
        print("name:{}, type:{}, degree:{}, visa:{}, url:{}".format(name,
                                                                    type,
                                                                    degree,
                                                                    visa,
                                                                    urls[i]))
        print(row[2])
        print("fetching logo . . .")
        print("Adding a company . . .")

        '''
        id INTEGER NOT NULL,
        name VARCHAR(100) NOT NULL,
        description VARCHAR,
        hiring_types INTEGER,
        hiring_majors VARCHAR,
        degree INTEGER,
        visa INTEGER,
        fair_id INTEGER,
        company_url VARCHAR,
        PRIMARY KEY (id),
        FOREIGN KEY(hiring_types) REFERENCES hiring_type (id),
        FOREIGN KEY(degree) REFERENCES degree_type (id),
        FOREIGN KEY(visa) REFERENCES visa_type (id),
        FOREIGN KEY(fair_id) REFERENCES fair (id)


        company [SQL: 'INSERT INTO company (name,
                description, hiring_types,
                hiring_majors, degree,
                visa, fair_id,
                company_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)']
                [parameters: ('ACTICO', None, 3, 'CS', 4, 2, 1, 'actico.com')]

        '''
        db_session = get_db_connection()
        company = Company(name=name, hiring_types=type, hiring_majors=row[2],
                          degree=degree, visa=visa, company_url=urls[i],
                          fair_id=1, description='')

        db_session.add(company)
        db_session.commit()


insert_rows()