import json
from configs import constants

with open(constants.INGEST_CONFIG, 'r') as f:
    config = json.load(f)
