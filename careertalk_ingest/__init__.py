from careertalk import db
from careertalk_ingest.ingest import CareerFairIngest
from careertalk_ingest.models import *
from common.config import IngestConfig

JOB = 'careertalk_ingest/ingest_jobs/uic-02132019-engineering-fair.json'
ingest = CareerFairIngest(IngestConfig(), db.session)
