import json

import pickle
import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.discovery import build


def _open_json(path):
    """
    :param path: This is path for the ingest-job.
    :return: Return python dictionary of ingest-job.

    TODO: later on we should be able to load multiple jobs at the same time.
    """
    with open(path, 'r') as f:
        ingest_job = json.load(f)
    return ingest_job


class GoogleSheet:
    """
    Google Sheet API wrapper class.
    """

    def __init__(self, ingest_config):
        self.config = ingest_config
        self.job = _open_json(ingest_config.work_path)

    def __repr__(self):
        return f"GoogleSheetConnection('job: {self.job}')"

    @property
    def gsheet_service(self):

        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        conf = self.config
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    conf.credentials, conf.scope)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build(conf.service, conf.discovery_version, credentials=creds)
        return service

    def get_employers(self):
        """

        :return: employers list
        """
        j = self.job
        employers = self.gsheet_service.spreadsheets().values().get(spreadsheetId=j['sheet_id'],
                                                             range=j['range']).execute()['values']
        return employers

    def get_urls(self):
        links = self.gsheet_service.spreadsheets().get(
            spreadsheetId=self.job['sheet_id'],
            ranges=self.job['range'],
            fields=self.config.sheet_link_field
        ).execute()
        links_rows = links['sheets'][0]['data'][0]['rowData']
        raw_urls = []
        for i, val in enumerate(links_rows):
            raw_urls.append(val['values'][0]['hyperlink'])

        return raw_urls
