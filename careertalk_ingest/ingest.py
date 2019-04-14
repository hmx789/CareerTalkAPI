import re
from datetime import datetime

from careertalk import create_ingest, db
from careertalk.models import Employer, CareerFairEmployer, CareerFair, College, Degree, HiringType
from careertalk_ingest.models import GoogleSheet

class CareerFairIngest:
    def __init__(self, ingest_config, debug=False):
        self.ingest_config = ingest_config
        self.gsheet = GoogleSheet(ingest_config)
        self.db_session = None
        self.url_pattern = re.compile('(//)(.+\.)(com|org|net|edu|gov|mil)')
        self.job = self.gsheet.job
        self.debug = debug

    def prune_www(self, url):
        """
        Takes raw url and then pic anything following www.
        If url does not contain www then return address follwing "//"

        ex)
        http://www.abc.com -> abc.com
        https://coffee.net -> coffee.net
        """
        match = self.url_pattern.search(url)
        new_url = match.group(2) + match.group(3)
        if 'www.' in match.group(2):
            return new_url[4:]
        return new_url

    def combine_fairs_urls(self, employers, urls):
        if len(employers) != len(urls):
            print("Something went wrong, number of employers and urls mismatch.")
            exit()

        for i, u in enumerate(urls):
            employers[i].append(self.prune_www(u))
        return employers

    # todo load employers by the careerfair_id from CareerFairEmployer
    # return the python dictionary "<employer_name>: <name>"
    def get_employers_id_set_from_db(self, careerfair_id):
        if self.db_session is None:
            print("This CareerFairIngest object does not have db session yet")
        employers = CareerFairEmployer.query.filter_by(careerfair_id=careerfair_id).all()
        if not employers:
            print("this careerfair does not have associated employers yet.")
            return None

        return set(e.employer_id for e in employers)

    def get_careerfair(self):
        """
        This method gets a career fair if exists on db, otherwise make careerfair and then return the fair.
        :return: CareerFair
        """
        fair_name = self.job['name']
        fair = CareerFair.query.filter_by(name=fair_name).first()
        if not fair:
            print("Creating a Career Fair {}".format(fair_name))
            fair = self.make_careerfair()
            self.add_data(fair, True)

        return fair

    def make_employer(self, name, url):
        # print("making employer")
        employer = Employer.query.filter_by(name=name).first()
        if employer:
            return employer
        return Employer(name=name, company_url=url)

    def get_employer(self, name):
        return Employer.query.filter_by(name=name).first()

    def get_org(self):
        college = College.query.filter_by(name=self.job['organization']).first()
        if not college:
            print("WARNING: This is unresolved dependency. Database administrator did not upload this college yet.")
        return college

    def make_careerfair(self):
        JOB = self.job
        college = self.get_org()
        name = JOB['name']
        # dates = [int(c) for c in JOB['date'].split('-')]
        dates = JOB['date']
        start_times = JOB['start_time']
        end_times = JOB['end_time']
        date = datetime(dates[0], dates[1], dates[2])
        start_time = datetime(dates[0], dates[1], dates[2], hour=start_times[0], minute=start_times[1])
        end_time = datetime(dates[0], dates[1], dates[2], hour=end_times[0], minute=end_times[1])
        location = JOB['location']
        address = JOB['address']
        city = JOB['city']
        zipcode = JOB['zipcode']
        careerfair = CareerFair(organization_id=college.id,
                                name=name,
                                date=date,
                                start_time=start_time,
                                end_time=end_time,
                                location=location,
                                address=address,
                                city=city,
                                zipcode=zipcode)
        return careerfair

    def get_degree_type_id(self, degree):
        degree_types = set(d.strip().lower() for d in degree.split(','))
        degree_types_sets_from_db = []
        degrees = Degree.query.all()
        for d in degrees:
            serial = d.serialize
            degree_types_sets_from_db.append(set(s.strip() for s in serial['type'].split(',')))
        degree_type_id = None
        for i, degree_tup in enumerate(degree_types_sets_from_db):
            if degree_types == degree_tup:
                degree_type_id = i + 1
        if not degree_type_id:
            print("Could not find that degree type: {} in our database.".format(degree))
        return degree_type_id

    def get_visa_type_id(self, visa_type):
        if visa_type == 'no':
            visa_type_id = 2
        elif visa_type == 'yes':
            visa_type_id = 1
        else:
            visa_type_id = 3
        return visa_type_id

    def get_hiring_type_id(self, hiring_type):
        hiring_types = [h.strip() for h in hiring_type.split(',')]
        if len(hiring_types) > 1:
            hiring_type_id = 3
        else:
            hiring_type_string = hiring_types[0].upper()
            hiring_type_id = HiringType.query.filter_by(type=hiring_type_string).first().id
        return hiring_type_id

    def make_careerfair_employer(self, columns, cf_id, e_id, tables):

        # This part might be redundant if we know how exactly string is formatted on the google sheet.
        visa_type = columns[0].lower()
        visa_type_id = self.get_visa_type_id(visa_type)
        degree_type_id = self.get_degree_type_id(columns[1])
        hiring_type_id = self.get_hiring_type_id(columns[2])

        hiring_majors = [m.strip() for m in columns[3].split(',')]
        hiring_majors_str = ', '.join(hiring_majors)

        return CareerFairEmployer(employer_id=e_id,
                                  careerfair_id=cf_id,
                                  visa_type_id=visa_type_id,
                                  degree_type_id=degree_type_id,
                                  hiring_majors=hiring_majors_str,
                                  hiring_type_id=hiring_type_id,
                                  tables=tables
                                  )

    def add_data(self, data, commit):
        if self.debug:
            print('debug mode is on, data is not inserted.')
            return False
        self.db_session.add(data)
        if commit:
            self.db_session.commit()
        return True

    def delete_data(self, data, commit):
        if self.debug:
            print('debug mode is on, data is not deleted.')
            return False
        self.db_session.delete(data)
        if commit:
            self.db_session.commit()
        return True

    def create_employer_to_table(self, row, fair_id):
        """
        This take a list that contains a single employer info in google sheet, create an employer obj,
        and then add the CareerFairEmployer to the careerfair_employer table.
        :param row: represents google sheet row.

        row[0]: Name of the employer
        row[1]: Hiring type
        row[2]: Majors
        row[3]: Degrees
        row[4]: Visa
        row[5]: Url
        Optional row[6]: tables <-- this one is optional.

        :return: name of the added employer
        """

        name = row[0]
        url = row[5]
        # row[4]=visa, row[3]=degree, row[2]=majors, row[1]=hiring_type
        selected_columns = (row[4], row[3], row[1], row[2])
        if len(row) < 7:
            tables = None
        else:
            tables = row[6]

        # insert Employer to the table.
        employer = self.get_employer(name)
        if not employer:
            employer = self.make_employer(name, url)
            self.add_data(employer, True)

        # insert CareerFairEmployer
        careerfair_employer = self.make_careerfair_employer(selected_columns,
                                                            fair_id,
                                                            employer.id,
                                                            tables)
        self.add_data(careerfair_employer, True)
        print("ADDED: {}, {}".format(name, url))

    def delete_non_participating_employers(self, ids_set):
        """
        :param employers_ids_set: set of employers ids
        :return: boolean
        """
        if not ids_set:
            return False

        for id in ids_set:
            careerfair_employer = CareerFairEmployer.query.filter_by(employer_id=id).first()
            employer = Employer.query.filter_by(id=id).first()
            print("DELETED: {}".format(employer.name))

            self.delete_data(careerfair_employer, True)

        return True

    def make_careerfair_employer_wrapper(self, fair_id, ids_set, rows):
        """
        :param fair_id: CareerFair id
        :param ids_set: employers_id set
        :param rows: Google sheet row
        :return: results of the parsing.
        """
        # CASE: This is new careerfair, add all the CareerFair employers.
        if not ids_set:
            for row in rows:
                self.create_employer_to_table(row, fair_id)
            return len(rows), 0, 0

        n_added = 0
        n_existing = len(ids_set)
        # CASE: Currently, there are some employers for this career fair.
        for i, row in enumerate(rows):
            employer_name = row[0]
            employer = self.get_employer(employer_name)

            if employer and employer.id in ids_set:
                ids_set.remove(employer.id)
                print("Exists Already {}: {}".format(i+1, employer.name))
                continue

            n_added += 1
            self.create_employer_to_table(row, fair_id)

        # employers in ids_set at this point should be removed from db from careerfair_employer table.
        n_deleted_employers = len(ids_set)
        # CASE: There were companies who decide not to participate.
        self.delete_non_participating_employers(ids_set)
        return n_added, n_existing-n_deleted_employers, n_deleted_employers

    def parse(self):
        print("parsing.")

        # cg is careerfair google sheet
        google_sheet = self.gsheet
        app = create_ingest(self.ingest_config)

        db.init_app(app)
        self.db_session = db.session

        careerfair_employer_rows = google_sheet.get_employers()
        urls = google_sheet.get_urls()
        rows = self.combine_fairs_urls(careerfair_employer_rows, urls)

        with app.app_context():
            careerfair = self.get_careerfair()
            employers_ids_set = self.get_employers_id_set_from_db(careerfair.id)
            n_added, n_existing, n_deleted = self.make_careerfair_employer_wrapper(careerfair.id, employers_ids_set, rows)

        print("\n===================================== RESULT =====================================")
        print("Sucesfully Parsed Googlesheet {}".format(self.job['sheet_id']))
        print("# New Employers      : {}".format(n_added))
        print("# Existing Employers : {}".format(n_existing))
        print("# Canceled Employers : {}\n".format(n_deleted))
        print("Link: {}\n".format(self.job['url']))
