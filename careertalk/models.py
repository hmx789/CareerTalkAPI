from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time
from careertalk import Base, db_session
from sqlalchemy.orm import relationship
from datetime import datetime


def _to_minutes(time):
    t = time.hour * 60 + time.minute
    return t


class Visa(Base):
    __tablename__ = 'visa_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(6), nullable=False)


class HiringType(Base):
    __tablename__ = 'hiring_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)


class Degree(Base):
    __tablename__ = 'degree_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    personal_email = Column(String(255), unique=True)
    profile_img = Column(String(), default='default_profile.png')
    registered_on = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.personal_email}')"

    @property
    def serialize(self):
        return {
            'personal_email': self.personal_email,
            'profile_url': self.profile_img,
            'registered_on': self.registered_on,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'id': self.id,
        }


class Employer(Base):
    __tablename__= 'employer'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    found_year = Column(String(4))
    hq_city = Column(String(50))
    description = Column(String())
    logo_url = Column(String(), default='default_employer.png')
    company_url = Column(String())

    def __repr__(self):
        return f"Employer('{self.name}', '{self.company_url}')"

    @property
    def serialize(self):
        return {
            'logo_url': self.logo_url,
            'company_url': self.company_url,
            'hq_city': self.hq_city,
            'found_year': self.found_year,
            'description': self.description,
            'name': self.name,
        }


class College(Base):
    __tablename__ = 'college'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    state_id = Column(Integer, ForeignKey('state.id'))
    city = Column(String(100))
    zipcode = Column(String(5))
    established = Column(Date)
    website = Column(String(255))
    logo_url = Column(String(255), default='default_college.png')

    def __repr__(self):
        return f"College('{self.name}')"

    @property
    def serialize(self):
        return {
            'logo_url': self.logo_url,
            'company_url': self.company_url,
            'hq_city': self.hq_city,
            'found_year': self.found_year,
            'description': self.description,
            'name': self.name,
        }


class CareerFairEmployer(Base):
    __tablename__ = 'employer_fair'
    id = Column(Integer, primary_key=True)
    employer_id = Column(Integer, ForeignKey('employer.id'), nullable=False)
    fair_id = Column(Integer, ForeignKey('fair.id'), nullable=False)
    recruiter_id = Column(Integer, ForeignKey('recruiter.id'))
    visa_type = Column(Integer, ForeignKey('visa_type.id'))
    degree_req = Column(Integer, ForeignKey('degree_type.id'), nullable=False)
    hiring_type = Column(Integer, ForeignKey('hiring_type.id'), nullable=False)
    hiring_majors = Column(String())
    tables = Column(String())

    def __repr__(self):
        return f"CareerFairEmployer('{self.hiring_majors}', '{self.employer_id}')"

    @property
    def serialize(self):
        degree = db_session.query(Degree).filter(Degree.id == self.degree_req).one()
        hiring_type = db_session.query(HiringType).filter(HiringType.id == self.hiring_type).one()
        visa = db_session.query(Visa).filter(Visa.id == self.visa_type).one()
        employer = db_session.query(Employer).filter(self.employer_id == Employer.id).one()
        majors = [major.strip() for major in self.hiring_majors.split(',')]
        degrees = [degree.strip() for degree in degree.type.split(',')]
        hiring_types = [hiring_type.strip() for hiring_type in hiring_type.type.split(',')]
        tables = [table.strip() for table in self.tables.split(',')] if self.tables is not None else []

        return {
            'tables': tables,
            'visa_support': visa.type,
            'hiring_majors': majors,
            'hiring_types': hiring_types,
            'degree_requirements': degrees,
            'employer': employer.serialize,
            'id': self.id
        }


class CareerFair(Base):
    __tablename__ = 'careerfair'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('college.id'))
    name = Column(String(100), nullable=False)
    description = Column(String)
    date = Column(DateTime, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    location = Column(String, nullable=False)
    address = Column(String(200))
    city = Column(String(50))
    zipcode = Column(String(5))
    other_organization = Column(String(50))
    employers = relationship(CareerFairEmployer, backref='careerfair', lazy=True)

    def __repr__(self):
        return f"Careerfair('{self.name}')"

    @property
    def serialize(self):
        # companies = [company.serialize for company in self.companies]
        return {
            'id': self.id,
            'name': self.name,
            'organization_id': self.organization_id,
            'description': self.description,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location,
            'address': self.address,
            'city': self.city,
            'zipcode': self.zipcode,
            'other_organization': self.other_organization
        }



# ------------------------------------------------------------------------------
#                                V1 models
# ------------------------------------------------------------------------------
class Fair(Base):
    __tablename__ = 'fair'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    location = Column(String)
    organization = Column(String(250))
    employers = relationship(CareerFairEmployer, backref='fair', lazy=True)

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


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String())
    hiring_types = Column(Integer, ForeignKey('hiring_type.id'))
    hiring_majors = Column(String())
    degree = Column(Integer, ForeignKey('degree_type.id'))
    visa = Column(Integer, ForeignKey('visa_type.id'))
    fair_id = Column(Integer, ForeignKey('fair.id'))
    company_url = Column(String())
    fair = relationship('Fair')

    @property
    def serialize(self):
        degree = [['BS'], ['MS'], ['PhD'], ['BS', 'MS'], ['BS', 'PhD'],
                  ['MS', 'PhD'], ['BS', 'MS', 'PhD']]
        types = [['INT'], ['FT'], ['INT', 'FT']]
        visa = ['yes', 'no', 'maybe']
        majors = [major.strip() for major in self.hiring_majors.split(',')]
        tables = db_session.query(CareerFairTable)\
            .filter(self.id == CareerFairTable.company_id)\
            .filter(self.fair_id == CareerFairTable.fair_id)\
            .all()

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


class CareerFairTable(Base):
    __tablename__ = 'fair_table'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.id'))
    fair_id = Column(Integer, ForeignKey('fair.id'))
    table_number = Column(Integer)
    fair = relationship('Fair')
    company = relationship('Company')
