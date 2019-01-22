from careertalk import app
from careertalk import config

if __name__ == "__main__":
    app.secret_key = config['DEFAULT']['SECRET_KEY']
    app.debug = True
    app.run()
