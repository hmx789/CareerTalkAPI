from flask import Flask
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

app = Flask(__name__)
with open('config.json', 'r') as f:
    config = json.load(f)


SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SPREADSHEET_ID = '1fKG4iVnj9coxg2mwip4reD7Rt5eiBvlEDM-Hu84M3zE'
RANGE_NAME = 'Sheet1!A4:E48'

def get_company_info():
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

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)

    return values

@app.route('/')
@app.route('/main')
def main():
    return "hello world"


if __name__ == "__main__":
    app.secret_key = config['DEFAULT']['SECRET_KEY']
    app.debug = True
    app.run()
