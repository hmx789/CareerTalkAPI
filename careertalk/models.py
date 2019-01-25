from careertalk import db
from datetime import datetime

def _to_minutes(time):
    t = time.hour * 60 + time.minute
    return t


class Visa(db.Model):
    __tablename__ = 'visa_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(6), nullable=False)


class HiringType(db.Model):
    __tablename__ = 'hiring_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)


class Degree(db.Model):
    __tablename__ = 'degree_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)


# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     middle_name = db.Column(db.String(50))
#     personal_email = db.Column(db.String(255), unique=True)
#     profile_img = db.Column(db.String(), default='default_profile.png')
#     registered_on = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return f"User('{self.first_name}', '{self.personal_email}')"
#
#     @property
#     def serialize(self):
#         return {
#             'personal_email': self.personal_email,
#             'profile_url': self.profile_img,
#             'registered_on': self.registered_on,
#             'first_name': self.first_name,
#             'last_name': self.last_name,
#             'middle_name': self.middle_name,
#             'id': self.id,
#         }
#
#
# class Employer(db.Model):
#     __tablename__= 'employer'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     found_year = db.Column(db.String(4))
#     hq_city = db.Column(db.String(50))
#     description = db.Column(db.String())
#     logo_url = db.Column(db.String(), default='default_employer.png')
#     company_url = db.Column(db.String())
#
#     def __repr__(self):
#         return f"Employer('{self.name}', '{self.company_url}')"
#
#     @property
#     def serialize(self):
#         return {
#             'logo_url': self.logo_url,
#             'company_url': self.company_url,
#             'hq_city': self.hq_city,
#             'found_year': self.found_year,
#             'description': self.description,
#             'name': self.name,
#         }
#
#
# class College(db.Model):
#     __tablename__ = 'college'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     address = db.Column(db.String(255))
#     state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
#     city = db.Column(db.String(100))
#     zipcode = db.Column(db.String(5))
#     established = db.Column(db.Date)
#     website = db.Column(db.String(255))
#     logo_url = db.Column(db.String(255), default='default_college.png')
#
#     def __repr__(self):
#         return f"College('{self.name}')"
#
#     @property
#     def serialize(self):
#         return {
#             'logo_url': self.logo_url,
#             'company_url': self.company_url,
#             'hq_city': self.hq_city,
#             'found_year': self.found_year,
#             'description': self.description,
#             'name': self.name,
#         }
#
#
# class CareerFairEmployer(db.Model):
#     __tablename__ = 'employer_fair'
#     id = db.Column(db.Integer, primary_key=True)
#     employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
#     fair_id = db.Column(db.Integer, db.ForeignKey('fair.id'), nullable=False)
#     recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'))
#     visa_type = db.Column(db.Integer, db.ForeignKey('visa_type.id'))
#     degree_req = db.Column(db.Integer, db.ForeignKey('degree_type.id'), nullable=False)
#     hiring_type = db.Column(db.Integer, db.ForeignKey('hiring_type.id'), nullable=False)
#     hiring_majors = db.Column(db.String())
#     tables = db.Column(db.String())
#
#     def __repr__(self):
#         return f"CareerFairEmployer('{self.hiring_majors}', '{self.employer_id}')"
#
#     @property
#     def serialize(self):
#         degree = Degree.query.filter_by(id=self.degree_req).first()
#         hiring_type = HiringType.query.filter_by(id=self.hiring_type)
#         visa = Visa.query.filter_by(id=self.visa_type)
#         employer = Employer.query.filter_by(id=self.employer_id)
#         # hiring_type = db_session.query(HiringType).filter(HiringType.id == self.hiring_type).one()
#         # visa = db_session.query(Visa).filter(Visa.id == self.visa_type).one()
#         # employer = db_session.query(Employer).filter(self.employer_id == Employer.id).one()
#         majors = [major.strip() for major in self.hiring_majors.split(',')]
#         degrees = [degree.strip() for degree in degree.type.split(',')]
#         hiring_types = [hiring_type.strip() for hiring_type in hiring_type.type.split(',')]
#         tables = [table.strip() for table in self.tables.split(',')] if self.tables is not None else []
#
#         return {
#             'tables': tables,
#             'visa_support': visa.type,
#             'hiring_majors': majors,
#             'hiring_types': hiring_types,
#             'degree_requirements': degrees,
#             'employer': employer.serialize,
#             'id': self.id
#         }
#
#
# class CareerFair(db.Model):
#     __tablename__ = 'careerfair'
#     id = db.Column(db.Integer, primary_key=True)
#     organization_id = db.Column(db.Integer, db.ForeignKey('college.id'))
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String)
#     date = db.Column(db.DateTime, nullable=False)
#     start_time = db.Column(db.Time, nullable=False)
#     end_time = db.Column(db.Time, nullable=False)
#     location = db.Column(db.String, nullable=False)
#     address = db.Column(db.String(200))
#     city = db.Column(db.String(50))
#     zipcode = db.Column(db.String(5))
#     other_organization = db.Column(db.String(50))
#     employers = db.relationship(CareerFairEmployer, backref='careerfair', lazy=True)
#
#     def __repr__(self):
#         return f"Careerfair('{self.name}')"
#
#     @property
#     def serialize(self):
#         # companies = [company.serialize for company in self.companies]
#         return {
#             'id': self.id,
#             'name': self.name,
#             'organization_id': self.organization_id,
#             'description': self.description,
#             'date': self.date,
#             'start_time': self.start_time,
#             'end_time': self.end_time,
#             'location': self.location,
#             'address': self.address,
#             'city': self.city,
#             'zipcode': self.zipcode,
#             'other_organization': self.other_organization
#         }
#


# ------------------------------------------------------------------------------
#                                V1 models
# ------------------------------------------------------------------------------
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String())
    hiring_types = db.Column(db.Integer, db.ForeignKey('hiring_type.id'))
    hiring_majors = db.Column(db.String())
    degree = db.Column(db.Integer, db.ForeignKey('degree_type.id'))
    visa = db.Column(db.Integer, db.ForeignKey('visa_type.id'))
    fair_id = db.Column(db.Integer, db.ForeignKey('fair.id'))
    company_url = db.Column(db.String())
    fair = db.relationship('Fair')

    @property
    def serialize(self):
        degree = [['BS'], ['MS'], ['PhD'], ['BS', 'MS'], ['BS', 'PhD'],
                  ['MS', 'PhD'], ['BS', 'MS', 'PhD']]
        types = [['INT'], ['FT'], ['INT', 'FT']]
        visa = ['yes', 'no', 'maybe']
        majors = [major.strip() for major in self.hiring_majors.split(',')]
        tables = CareerFairTable.query.filter_by(id=self.id, fair_id=self.fair_id).all()

        # tables = db_session.query(CareerFairTable)\
        #     .filter(self.id == CareerFairTable.company_id)\
        #     .filter(self.fair_id == CareerFairTable.fair_id)\
        #     .all()

        tables_list = [t.table_number for t in tables]

        return {
            'tables': tables_list,
            'fair': self.fair.name,
            'fair_id': self.fair_id,
            'visa': visa[self.visa-1],
            'degree': degree[self.degree-1],
            'hiring_majors': majors,
            'hiring_types': types[self.hiring_types-1],
            'description': self.description,
            'company_url': self.company_url,
            'name': self.name,
            'id': self.id,
        }


class CareerFairTable(db.Model):
    __tablename__ = 'fair_table'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    fair_id = db.Column(db.Integer, db.ForeignKey('fair.id'))
    table_number = db.Column(db.Integer)
    fair = db.relationship('Fair')
    company = db.relationship('Company')

class Fair(db.Model):
    __tablename__ = 'fair'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String)
    organization = db.Column(db.String(250))

    def __repr__(self):
        return f"Fair('{self.name}', '{self.employer_id}')"

    @property
    def serialize(self):
        # companies = [company.serialize for company in self.companies]
        return {
            'id': self.id,
            'name': self.name,
            'organization': self.organization,
            'description': self.description,
            'location': self.location,
            'date': {
                'year': self.start_date.year,
                'month': self.start_date.month,
                'day': self.start_date.day
            },
            'start_date_min': self.start_date,
            'end_date': self.end_date,
            'start_time_min': _to_minutes(self.start_time),
            'end_time': _to_minutes(self.end_time)
        }


