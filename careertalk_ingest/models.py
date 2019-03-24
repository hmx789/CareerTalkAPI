import json

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def _open_jobs(path):
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
    SHEET_LINK_FIELD = 'sheets/data/rowData/values/hyperlink'

    def __init__(self, ingest_config):
        self.config = ingest_config
        self.job = _open_jobs(self.config.work_path)
        self.service = self.gsheet_service

    def __repr__(self):
        return f"GoogleSheetConnection('job: {self.job}')"

    @property
    def gsheet_service(self):
        conf = self.config
        store = file.Storage(conf.token_path)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(conf.cred_path, conf.scope)
            creds = tools.run_flow(flow, store)

        return build(conf.service,
                     conf.discovery_version,
                     http=creds.authorize(Http()))

    def get_employers(self):
        j = self.job
        employers = self.service.spreadsheets().values().get(spreadsheetId=j['sheet_id'],
                                                             range=j['range']).execute()['values']
        return employers

    def get_urls(self):
        links = self.service.spreadsheets().get(
            spreadsheetId=self.job['sheet_id'],
            ranges=self.job['range'],
            fields=self.SHEET_LINK_FIELD
        ).execute()
        links_rows = links['sheets'][0]['data'][0]['rowData']
        raw_urls = []
        for i, val in enumerate(links_rows):
            raw_urls.append(val['values'][0]['hyperlink'])

        return raw_urls
