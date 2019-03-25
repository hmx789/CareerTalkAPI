import sys

from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("ERROR: Please provide an argument.")
        print("Example: python run.py ingest")
        exit()

    if sys.argv[1] == 'ingest':
        from careertalk_ingest import ingest

        print("Start Data Ingestion")
        ingest.parse()

    if sys.argv[1] == 'load':
        from careertalk_load import load

        print("Start Data Load")
        if (load.load_schema()):
            print("Sucesfully Created Schema")
            print("Starting Data Insertion")
            load.insert_values()
            print("Finished Data Insertion")

    if sys.argv[1] == 'app':
        # TODO: Currently, the app is calling routes and __init__.py twice.
        print("before loading app")
        from careertalk import app, db
        print("after loading app")
        from careertalk_cron.cron_jobs import calculate_top5
        print("careertalk cron job loaded")
        import careertalk.routes

        sched = BackgroundScheduler()
        sched.start()
        print("adding cron job.")
        sched.add_job(calculate_top5, 'interval', hours=5, args=[db.session])

        print("app run!!")
        app.run(debug=True)
