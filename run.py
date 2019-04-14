import sys

from apscheduler.schedulers.background import BackgroundScheduler
from careertalk import create_load, create_rest, db
from common.config import IngestConfig

if __name__ != "__main__":
    exit()

if len(sys.argv) == 0:
    print("ERROR: Please provide an argument.")
    print("Example: python run.py ingest")
    exit()

if sys.argv[1] == 'ingest':
    ingest_config = IngestConfig()

    from careertalk_ingest.ingest import CareerFairIngest

    ingest = CareerFairIngest(ingest_config=ingest_config)
    print("Start Data Ingestion")
    ingest.parse()

if sys.argv[1] == 'load':
    from careertalk_load.models import LoadDataIntoPostgres
    from common.config import LoadConfig

    load_config = LoadConfig()
    app = create_load(load_config)

    load = LoadDataIntoPostgres(load_config, db)
    print("Start Data Load")
    if (load.load_schema()):
        print("Sucesfully Created Schema")
        print("Starting Data Insertion")
        load.insert_values()
        print("Finished Data Insertion")

if sys.argv[1] == 'app':
    from careertalk_cron.cron_jobs import calculate_top5

    ingest_config = IngestConfig()
    app = create_rest(ingest_config)
    scheduler = BackgroundScheduler()

    print("adding cron job.")

    from careertalk_ingest.ingest import CareerFairIngest

    ingest = CareerFairIngest(ingest_config=ingest_config)
    print("Start Data Ingestion")

    scheduler.add_job(calculate_top5, 'interval', hours=5, args=[db.session])
    scheduler.add_job(ingest.parse, 'interval', hours=6)
    print("App run!")
    scheduler.start()

    app.run(debug=True, use_reloader=False)
