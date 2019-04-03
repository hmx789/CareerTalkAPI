import sys

from apscheduler.schedulers.background import BackgroundScheduler
from careertalk import create_rest, create_load, create_ingest
from common.config import IngestConfig

if __name__ != "__main__":
    exit()

if len(sys.argv) == 0:
    print("ERROR: Please provide an argument.")
    print("Example: python run.py ingest")
    exit()

if sys.argv[1] == 'ingest':
    ingest_config = IngestConfig()
    app, db = create_ingest(ingest_config)

    from careertalk_ingest.ingest import CareerFairIngest

    ingest = CareerFairIngest(ingest_config=ingest_config, db_session=db.session)
    print("Start Data Ingestion")
    ingest.parse()

if sys.argv[1] == 'load':
    from careertalk_load.models import LoadDataIntoPostgres
    from common.config import LoadConfig

    load_config = LoadConfig()
    app, db = create_load(load_config)

    load = LoadDataIntoPostgres(load_config, db)
    print("Start Data Load")
    if (load.load_schema()):
        print("Sucesfully Created Schema")
        print("Starting Data Insertion")
        load.insert_values()
        print("Finished Data Insertion")

if sys.argv[1] == 'app':
    from common.config import Config
    from careertalk_cron.cron_jobs import calculate_top5

    config = Config()
    app, db = create_rest(config)
    scheduler = BackgroundScheduler()
    scheduler.start()
    print("adding cron job.")

    scheduler.add_job(calculate_top5, 'interval', hours=5, args=[db.session])
    print("App run!")

    app.run()
