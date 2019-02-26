from careertalk import app
from careertalk_ingest import ingest
from careertalk_load import load
import sys


if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("ERROR: Please provide an argument.")
        print("Example: python run.py ingest")
        exit()

    if sys.argv[1] == 'ingest':
        print("Start Data Ingestion")
        ingest.parse()

    if sys.argv[1] == 'load':
        print("Start Data Load")
        if(load.load_schema()):
            print("Sucesfully Created Schema")
            load.insert_values()


    if sys.argv[1] == 'app':
        app.run(debug=True)
