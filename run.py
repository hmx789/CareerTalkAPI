import sys

from careertalk import app

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
        app.run(debug=True)
