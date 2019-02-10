from careertalk import app
import sys

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("ERROR: Please provide an argument.")
        print("Example: python run.py ingest")
        exit()

    if sys.argv[1] == 'ingest':
        print("Begin Data Ingestion")

    if sys.argv[1] == 'app':
        app.run(debug=True)
