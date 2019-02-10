import json
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from httplib2 import Http


def _get_config(path):
    with open(path, 'r') as f:
        config = json.load(f)
    return config


class GoogleSheetConnection:
    def __init__(self, ingest_config_path, work_path):
        self.config = _get_config(ingest_config_path)['gsheet']
        self.job = _get_config(work_path)
        self.ingest_config_path = ingest_config_path
        self.work_path = work_path

    def __repr__(self):
        return f"GoogleSheetConnection('" \
            f"config: {self.config}', " \
            f"'job: {self.job}', " \
            f"'config_path: {self.ingest_config_path}', " \
            f"'work_path: {self.work_path}')"

    def _get_service(self):
        store = file.Storage(self.config['token'])
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.ingest_config_path,
                                                  self.config['scope'])
            creds = tools.run_flow(flow, store)

        service = build(self.config['service'],
                        self.config['discovery_version'],
                        http=creds.authorize(Http()))
        return service


# Super Mini Manual Test.
print(GoogleSheetConnection('/Users/seholim/computerscientist/creativelabs/forked/CareerTalkAPI/configs/ingest-config.json','/Users/seholim/computerscientist/creativelabs/forked/CareerTalkAPI/careertalk_ingest/ingest_jobs/uic-02132019-engineering-fair.json'))