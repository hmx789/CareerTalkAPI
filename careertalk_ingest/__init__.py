from careertalk_ingest.models import *
from configs import constants
from careertalk import db

JOB = 'careertalk_ingest/ingest_jobs/uic-02132019-engineering-fair.json'
ingest = CareerFairIngest(constants.INGEST_CONFIG, JOB, db.session)