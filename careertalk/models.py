import uuid

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

def _to_minutes(time):
    t = time.hour * 60 + time.minute
    return t


def _format_time(time):
    suffix = 'PM' if time.hour >= 12 else 'AM'
    hour = time.hour - 12 if time.hour >= 13 else time.hour
    return "{}:{} {}".format(hour, time.strftime("%M"), suffix)


class Visa(db.Model):
    __tablename__ = 'visa_type'
    id = db.Column(db.Integer, primary_key=True)
    type = Column(db.String(6), nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'type': self.type.lower()
        }

    def get_visa_id(self, visa_type):
        lower = visa_type.lower()
        visas = Visa.query.all()
        for v in visas:
            visa = v.serialize
            if visa.type == lower:
                return visa.id
        print("Could not find {} in Visa".format(visa_type))
        return None


class HiringType(db.Model):
    __tablename__ = 'hiring_type'
    id = db.Column(db.Integer, primary_key=True)
    type = Column(db.String(20), nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'type': self.type.lower()
        }

    def get_hiring_id(self, hiring_type):
        lower = hiring_type.lower()
        hiring_types = self.query.all()
        for h in hiring_types:
            hiring = h.serialize
            if [s.strip() for s in hiring.type.split] == [s.strip() for s in lower.split(',')]:
                return hiring.id
        print("Could not find {} in HiringType".format(hiring_type))
        return None


class Degree(db.Model):
    __tablename__ = 'degree_type'
    id = db.Column(db.Integer, primary_key=True)
    type = Column(db.String(20), nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'type': self.type.lower()
        }

    def get_degree_id(self, degree_type):
        lower = degree_type.lower()
        degress = self.query.all()
        for d in degress:
            degree = d.serialize
            if [s.strip() for s in degree.type.split] == [s.strip() for s in lower.split(',')]:
                return degree.id
        print("Could not find {} in Degree".format(degree_type))
        return None


class User(db.Model):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    google_id = Column(db.String(255))
    first_name = Column(db.String(50), nullable=False)
    last_name = Column(db.String(50), nullable=False)
    middle_name = Column(db.String(50))
    personal_email = Column(db.String(255))
    profile_img = Column(db.String(), default='default_profile.png')
    registered_on = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.personal_email}')"

    @property
    def serialize(self):
        return {
            'personal_email': self.personal_email,
            'google_id': self.google_id,
            'profile_url': self.profile_img,
            'registered_on': self.registered_on,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'id': str(self.id),
        }


class Connection(db.Model):
    __tablename__ = 'connection'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    user_id = Column(UUID, db.ForeignKey('user.id'))
    public_id = Column(db.String(255))
    access_token = Column(db.String(255))
    secret = Column(db.String(255))
    id_token = Column(db.String(255))
    token = Column(db.String)
    os = Column(db.String(10))

    def __repr__(self):
        return f"Connection('{self.id}', '{self.user_id}')"


class Recruiter(db.Model):
    __tablename__ = 'recruiter'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    first_name = Column(db.String(100), nullable=False)
    last_name = Column(db.String(100), nullable=False)
    middle_name = Column(db.String(100))
    employer_id = Column(UUID, db.ForeignKey('employer.id'))
    work_email = Column(db.String(255))
    work_phone = Column(db.String(16))

    def __repr__(self):
        return f"Recruiter('{self.first_name}')"

    @property
    def serialize(self):
        return {
            'email': self.work_email,
            'phone': self.work_phone,
            'profile_url': self.profile_img,
            'registered_on': self.registered_on,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'id': self.id
        }


class Employer(db.Model):
    __tablename__ = 'employer'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    name = Column(db.String(100), nullable=False)
    found_year = Column(db.String(4))
    hq_city = Column(db.String(50))
    description = Column(db.String())
    logo_url = Column(db.String(), default='default_employer.png')
    company_url = Column(db.String())

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
            'id': self.id
        }


class Student(db.Model):
    __tablename__ = 'student'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    user_id = Column(UUID, db.ForeignKey('user.id'), nullable=False)
    college_id = Column(UUID, db.ForeignKey('college.id'))
    looking_hiring_type = Column(db.Integer, db.ForeignKey('hiring_type.id'))
    degree = Column(db.Integer, db.ForeignKey('degree_type.id'))
    graduating_date = Column(db.Date)
    available_date = Column(db.Date)
    github_link = Column(db.String(255))
    linkedin_link = Column(db.String(255))
    portfolio_link = Column(db.String(255))
    school_email = Column(db.String(255))
    major = Column(db.String(50))

    def __repr__(self):
        return f"Student(user_id: '{self.user_id}')"

    @property
    def serialize(self):
        user = User.query.filter_by(uuid=self.user_id).first()
        college = College.query.filter_by(uuid=self.college_id).first()
        college_name = 'None' if not college else college.name
        pursuing_degree_id = Degree.query.filter_by(id=self.degree).first()
        pursuing_hiring_type = HiringType.query.filter_by(id=self.looking_hiring_type).first()

        majors = None
        if self.major:
            majors = [major for major in self.major.split(',')]

        return {
            'persuing_work_type': pursuing_hiring_type,
            'school_email': self.school_email,
            'portfolio_link': self.portfolio_link,
            'linkedin_link': self.linkedin_link,
            'github_link': self.github_link,
            'available_date': self.available_date,
            'graduating_date': self.graduating_date,
            'major': majors,
            'persuing_degree': pursuing_degree_id,
            'college_name': college_name,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'id': self.id
        }


class College(db.Model):
    __tablename__ = 'college'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    name = Column(db.String(255))
    address = Column(db.String(255))
    city = Column(db.String(100))
    zipcode = Column(db.String(5))
    state = Column(db.String(2))
    established = Column(db.Date)
    website = Column(db.String(255))
    logo_url = Column(db.String(255), default='default_college.png')

    def __repr__(self):
        return f"College('{self.name}')"

    @property
    def serialize(self):
        return {
            'logo_url': self.logo_url,
            'web_url': self.website,
            'established': self.established,
            'state': self.state,
            'zipcode': self.zipcode,
            'city': self.city,
            'address': self.address,
            'name': self.name,
            'id': self.id
        }


class CareerFairEmployer(db.Model):
    __tablename__ = 'careerfair_employer'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"), )
    employer_id = Column(UUID, db.ForeignKey('employer.id'), nullable=False)
    careerfair_id = Column(UUID, db.ForeignKey('careerfair.id'), nullable=False)
    recruiter_id = Column(UUID, db.ForeignKey('recruiter.id'))
    visa_type_id = Column(db.Integer, db.ForeignKey('visa_type.id'))
    degree_type_id = Column(db.Integer, db.ForeignKey('degree_type.id'), nullable=False)
    hiring_type_id = Column(db.Integer, db.ForeignKey('hiring_type.id'), nullable=False)
    hiring_majors = Column(db.String())
    tables = Column(db.String())

    def __repr__(self):
        return f"CareerFairEmployer('{self.hiring_majors}', '{self.employer_id}')"

    @property
    def serialize(self):
        degree = Degree.query.filter_by(id=self.degree_type_id).first()
        hiring_type = HiringType.query.filter_by(id=self.hiring_type_id).first()
        hiring_types = [hiring_type.strip() for hiring_type in hiring_type.type.split(',')]
        visa = Visa.query.filter_by(id=self.visa_type_id).first()
        employer = Employer.query.filter_by(id=self.employer_id).first()
        majors = [major.strip() for major in self.hiring_majors.split(',')]
        degrees = [degree.strip() for degree in degree.type.split(',')]
        tables = [table.strip() for table in self.tables.split(',')] if self.tables is not None else []

        return {
            'tables': tables,
            'visa_support': visa.type,
            'hiring_majors': majors,
            'hiring_types': hiring_types,
            'degree_requirements': degrees,
            'employer': employer.serialize,
            'careerfair_id': self.careerfair_id,
            'id': self.id
        }


class CareerFair(db.Model):
    __tablename__ = 'careerfair'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    organization_id = Column(UUID, db.ForeignKey('college.id'))
    name = Column(db.String(100), nullable=False)
    description = Column(db.String)
    date = Column(db.DateTime, nullable=False)
    start_time = Column(db.Time, nullable=False)
    end_time = Column(db.Time, nullable=False)
    location = Column(db.String, nullable=False)
    address = Column(db.String(200))
    city = Column(db.String(50))
    zipcode = Column(db.String(5))
    other_organization = Column(db.String(50))
    map_url = Column(db.String())
    employers = db.relationship(CareerFairEmployer, backref='careerfair', cascade='all,delete', lazy=True)

    def __repr__(self):
        return f"Careerfair('{self.name}')"

    @property
    def serialize(self):
        formatted_start_time = _format_time(self.start_time)
        formatted_end_time = _format_time(self.end_time)
        return {
            'id': self.id,
            'name': self.name,
            'organization_id': self.organization_id,
            'description': self.description,
            'date': self.date.strftime("%m/%d/%Y"),
            'start_time': formatted_start_time,
            'end_time': formatted_end_time,
            'location': self.location,
            'address': self.address,
            'city': self.city,
            'zipcode': self.zipcode,
            'other_organization': self.other_organization,
            'map_url': self.map_url,
            'num_of_employers': len(self.employers)
        }


class Like(db.Model):
    __tablename__ = 'student_like_employer'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    student_id = Column(UUID, db.ForeignKey('student.id'), nullable=False)
    employer_id = Column(UUID, db.ForeignKey('employer.id'), nullable=False)
    careerfair_id = Column(UUID, db.ForeignKey('careerfair.id'))

    def __repr__(self):
        return f"Like('{self.id}')"


class Top5(db.Model):
    __tablename__ = 'top_five_employers'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    top1 = Column(UUID, db.ForeignKey('employer.id'))
    top2 = Column(UUID, db.ForeignKey('employer.id'))
    top3 = Column(UUID, db.ForeignKey('employer.id'))
    top4 = Column(UUID, db.ForeignKey('employer.id'))
    top5 = Column(UUID, db.ForeignKey('employer.id'))
    careerfair_id = Column(UUID, db.ForeignKey('careerfair.id'))
    updated_on = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Top5('{self.id}')"

    @property
    def serialize(self):
        employer1 = Employer.query.filter_by(uuid=self.top1).first()
        employer2 = Employer.query.filter_by(uuid=self.top2).first()
        employer3 = Employer.queryfilter_by(uuid=self.top3).first()
        employer4 = Employer.queryfilter_by(uuid=self.top4).first()
        employer5 = Employer.queryfilter_by(uuid=self.top5).first()
        careerfair = CareerFair.queryfilter_by(uuid=self.careerfair_id).first()

        return {
            'top1': employer1.serialize,
            'top2': employer2.serialize,
            'top3': employer3.serialize,
            'top4': employer4.serialize,
            'top5': employer5.serialize,
            'careerfair': careerfair.serialize
        }


# ------------------------------------------------------------------------------
#                                V1 models
# ------------------------------------------------------------------------------


class Company(db.Model):
    __tablename__ = 'company'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    name = Column(db.String(100), nullable=False)
    description = Column(db.String())
    hiring_types = Column(db.Integer, db.ForeignKey('hiring_type.id'))
    hiring_majors = Column(db.String())
    degree = Column(db.Integer, db.ForeignKey('degree_type.id'))
    visa = Column(db.Integer, db.ForeignKey('visa_type.id'))
    fair_id = Column(UUID, db.ForeignKey('fair.id'))
    company_url = Column(db.String())

    @property
    def serialize(self):
        degree = [['BS'], ['MS'], ['PhD'], ['BS', 'MS'], ['BS', 'PhD'],
                  ['MS', 'PhD'], ['BS', 'MS', 'PhD']]
        types = [['INT'], ['FT'], ['INT', 'FT']]
        visa = ['yes', 'no', 'maybe']
        majors = [major.strip() for major in self.hiring_majors.split(',')]
        tables = CareerFairTable.query.filter_by(fair_id=self.fair_id).all()

        tables_list = [t.table_number for t in tables]

        return {
            'tables': tables_list,
            'fair': self.fair.name,
            'fair_id': self.fair_id,
            'visa': visa[self.visa - 1],
            'degree': degree[self.degree - 1],
            'hiring_majors': majors,
            'hiring_types': types[self.hiring_types - 1],
            'description': self.description,
            'company_url': self.company_url,
            'name': self.name,
            'id': self.id,
        }


class CareerFairTable(db.Model):
    __tablename__ = 'fair_table'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    company_id = Column(UUID, db.ForeignKey('company.id'))
    fair_id = Column(UUID, db.ForeignKey('fair.id'))
    table_number = Column(db.Integer)
    fair = db.relationship('Fair')
    company = db.relationship('Company')

class Fair(db.Model):
    __tablename__ = 'fair'
    id = Column(UUID(as_uuid=True),  primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    name = Column(db.String(100), nullable=False)
    description = Column(db.String)
    start_date = Column(db.Date, nullable=False)
    end_date = Column(db.Date, nullable=False)
    start_time = Column(db.Time, nullable=False)
    end_time = Column(db.Time, nullable=False)
    location = Column(db.String)
    organization = Column(db.String(250))
    companies = db.relationship('Company', backref='fair', cascade="all,delete", lazy=True)

    def __repr__(self):
        return f"Fair('{self.name}', '{self.employer_id}')"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        companies = [company.serialize for company in self.companies]
        return {
            'id': self.id,
            'name': self.name,
            'organization': self.organization,
            'description': self.description,
            'companies': companies,
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
