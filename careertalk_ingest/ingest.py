import re
from datetime import datetime

from careertalk.models import Employer, CareerFairEmployer, CareerFair, College, Degree, HiringType
from careertalk_ingest.models import GoogleSheet


class CareerFairIngest:
    def __init__(self, ingest_config, db_session=None, debug=False):
        self.gsheet = GoogleSheet(ingest_config)
        self.db_session = db_session
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
        return CareerFair.query.filter_by(name=self.job['name']).first()

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

    def add_employer_to_table(self, row, fair_id):
        """
        This take a list that contains a single employer info in google sheet and add the company to the db.
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
            print("No table information")
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
        print("ADDED {}: {}".format(name, url))

    def delete_non_participating_employers(self, employers_ids_set):
        if not employers_ids_set:
            return False

        for id in employers_ids_set:
            employer = CareerFairEmployer.query.filter_by(employer_id=id)
            self.delete_data(employer, False)
        self.db_session.commit()
        return True
    
    def parse(self):
        # cg is careerfair google sheet
        cgs = self.gsheet
        careerfair_employe_rows = cgs.get_employers()
        urls = cgs.get_urls()
        if len(careerfair_employe_rows) != len(urls):
            print("Something went wrong, number of employers and urls mismatch.")
            exit()

        careerfair_employe_rows = self.combine_fairs_urls(careerfair_employe_rows, urls)
        careerfair = self.get_careerfair()
        print(careerfair)
        if not careerfair:
            print("Creating a Career Fair")
            careerfair = self.make_careerfair()
            self.add_data(careerfair, True)

        # todo here finish the logic: when employers and the careerfair exist
        employers_ids_set = self.get_employers_id_set_from_db(careerfair.id)

        for row in careerfair_employe_rows:
            company_name = row[0]
            if employers_ids_set and company_name in employers_ids_set:
                employers_ids_set.pop(company_name)
                print("{} already exists".format(company_name))
                continue
            print("New company {} is joining {}!".format(company_name, careerfair.name))

            # create a wrapper function that wraps make_careerfair_employer
            self.add_employer_to_table(row, careerfair.id)

        # CASE: There were companies who decide not to participate.
        self.delete_non_participating_employers(employers_ids_set)

        print("Sucesfully Parsed Googlesheet {}".format(self.job['sheet_id']))
