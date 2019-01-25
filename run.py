from careertalk import app
from careertalk import config

if __name__ == "__main__":
    app.secret_key = config['default']['secret_key']
    app.config['JWT_SECRET_KEY'] = app.secret_key  # Change this!
    app.config['social_facebook'] = {
        'app_id': config['social']['facebook']['app_id'],
        'app_secret': config['social']['facebook']['app_secret']
    }

    app.config['social_google'] = {
        'client_id': config['social']['google']['client_id'],
        'client_secret': config['social']['google']['client_secret']
    }

    app.debug = True
    app.run()
