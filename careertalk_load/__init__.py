from careertalk import db

class LoadDataIntoPostgres:
    def load_schema(self):
        db.create_all()
        return 1

load = LoadDataIntoPostgres()


