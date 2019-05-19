import sys
import os

from apscheduler.schedulers.background import BackgroundScheduler
from common.config import IngestConfig
from careertalk import create_rest

env = os.environ
ingest_config = IngestConfig()
app = create_rest(ingest_config)

if (len(sys.argv) > 1 and sys.argv[1] == 'app') or env.get('DEBUG') == 'False':
    print("Starting App")
    from careertalk_cron.cron_jobs import calculate_top5

    scheduler = BackgroundScheduler()

    from careertalk_ingest.ingest import CareerFairIngest

    ingest = CareerFairIngest(ingest_config=ingest_config)

    # print("Adding Two Cron Jobs")
    # scheduler.add_job(calculate_top5, 'interval', hours=5)
    # scheduler.add_job(ingest.parse, 'interval', hours=12)
    # scheduler.start()
    app.run(debug=True, use_reloader=False)

if len(sys.argv) == 2:

    if sys.argv[1] == 'ingest':
        from careertalk_ingest.ingest import CareerFairIngest

        ingest_config = IngestConfig()

        ingest = CareerFairIngest(ingest_config=ingest_config)

        print("Start Data Ingestion")
        ingest.parse()

    if sys.argv[1] == 'load':
        from careertalk_load.models import LoadDataIntoPostgres
        from common.config import LoadConfig

        load_config = LoadConfig()
        load = LoadDataIntoPostgres(load_config)
        load.load_schema_using_alchemy()
