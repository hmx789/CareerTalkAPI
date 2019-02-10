from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from careertalk import db
import re, json
import sys

# -----------------------------------------------------------------------------
#                           Global Constants
# -----------------------------------------------------------------------------
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SPREADSHEET_ID = '1ngKTclEJo4m9D_TY4VwwOqDNa13CubbNmwQ20QJrOpE'
RANGE_NAME = 'Sheet1!A4:F110'
FAIR_ID = 2
DEBUG = 0

if len(sys.argv) > 1:
    if str(sys.argv[1]) == "-d":
        print('*** DEBUG MODE IS ON ***')
        DEBUG = 1
else :
    print('*** PRODUCTION MODE IS ON ***')

with open('{}/config.json'.format(parent_dir), 'r') as f:
    config = json.load(f)

postgres = config["POSTGRES"]

engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
                                                postgres["user"],
                                                postgres["pw"],
                                                postgres["endpoint"],
                                                postgres["port"],
                                                postgres["db"]),
                                            connect_args={'sslmode':'require'})

# -----------------------------------------------------------------------------
#                           Parsing Functions
# -----------------------------------------------------------------------------


def get_db_connection():
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()
    return db_session


def _add_tables(name, s, session):
    if len(s) == 0:
        print('***Warning: No Table')
        return
    print("ADDING TABLES")
    booths = [int(c.strip()) for c in s.split('&')]
    company = session.query(Company).filter(Company.name == name).filter(
        Company.fair_id == FAIR_ID).one()
    for t in booths:
        table = CareerFairTable(fair_id=FAIR_ID, company_id=company.id,
                                table_number=t)
        print('TABLE: fair: {}, company: {}, number: {}'.format(FAIR_ID,
                                                                company.id,
                                                                t))
        if not DEBUG:
            session.add(table)
    if not DEBUG:
        session.commit()


def match_company_url(raw_url, pattern):
    matches = pattern.finditer(raw_url)
    url = ''
    for m in matches:
        url = m.group(2) + m.group(3)
        if 'www.' in m.group(2):
            url = url[4:]
    return url


def get_company_info():

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
    # print(values)
    for i, val in enumerate(links_rows):
        raw_url = val['values'][0]['hyperlink']
        url = match_company_url(raw_url, pattern)
        values[i].append(url)
        # print(values[i])
    return values


def insert_rows():
    data = get_company_info()
    print("Adding a company . . .")
    db_session = get_db_connection()

    companies_in_db = db_session.query(Company).\
                                    filter(Company.fair_id == FAIR_ID).all()


    companies_dict = {}

    # Construct {'name': 0 || 1} dictionary
    for c in companies_in_db:
        companies_dict[c.name] = 0

    for i, row in enumerate(data):
        name, url = row[0], row[4]
        companies_dict[name] = 1 if name in companies_dict else 0

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
        print(row)
        #_add_tables_temp(name, row[5], db_session)
        if companies_dict[name] == 1:
            print("WARNING: {}:{} already exists in our db.".format(i+1, name))
            continue
        log_string = '''name:{}, type:{}, degree:{}, visa:{}, booth:{} url:{}
        '''.format(name, type, degree, visa, row[5], row[6])
        print("**ADDING: {}".format(log_string))
        company = Company(name=name, hiring_types=type, hiring_majors=row[2],
                          degree=degree, visa=visa, company_url=row[6],
                          fair_id=FAIR_ID, description='')
        if not DEBUG:
            db_session.add(company)
            db_session.commit()
        _add_tables(name, row[5], db_session)
        companies_dict[name] = 1


    # delete not participating companies
    print('Seraching Companies that are no longer participating in ', FAIR_ID)
    for key, val in companies_dict.items():
        if val == 0:
            print('Deleting company {} on fair: {}'.format(key, FAIR_ID))
            c = db_session.query(Company).filter(Company.name == key).filter(
                Company.fair_id == FAIR_ID).one()

            t = db_session.query(CareerFairTable)\
                .filter(c.id == CareerFairTable.company_id)\
                .filter(c.fair_id == CareerFairTable.fair_id)\
                .all()
            for table in t:
                print('Deleting table {} on fair: {}'.format(table.id, FAIR_ID))
                if not DEBUG:
                    db_session.delete(table)
            if not DEBUG:
                db_session.delete(c)
            db_session.commit()
    db_session.close()


insert_rows()
