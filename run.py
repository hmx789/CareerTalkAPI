from careertalk import app
from careertalk_ingest import ingest
import sys

"""
from flask import Flask

 
app = Flask(__name__)
 
 
#add your job here
 
'''
All of your app.routes here
'''
 
# finally

if __name__ == "__main__":
	app.run()


"""




if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("ERROR: Please provide an argument.")
        print("Example: python run.py ingest")
        exit()

    if sys.argv[1] == 'ingest':
        print("Begin Data Ingestion")
        ingest.parse()


    if sys.argv[1] == 'app':
        app.run(debug=True)
