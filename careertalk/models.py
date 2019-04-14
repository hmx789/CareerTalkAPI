from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

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
    type = db.Column(db.String(6), nullable=False)

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
    type = db.Column(db.String(20), nullable=False)

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
    type = db.Column(db.String(20), nullable=False)

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
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    personal_email = db.Column(db.String(255), unique=True)
    profile_img = db.Column(db.String(), default='default_profile.png')
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

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


class Connection(db.Model):
    __tablename__ = 'connection'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    public_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    id_token = db.Column(db.String(255))
    token = db.Column(db.String)
    os = db.Column(db.String(10))

    def __repr__(self):
        return f"Connection('{self.id}', '{self.user_id}')"


class Recruiter(db.Model):
    __tablename__ = 'recruiter'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'))
    work_email = db.Column(db.String(255))
    work_phone = db.Column(db.String(16))

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
            'id': self.id,
        }


class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    found_year = db.Column(db.String(4))
    hq_city = db.Column(db.String(50))
    description = db.Column(db.String())
    logo_url = db.Column(db.String(), default='default_employer.png')
    company_url = db.Column(db.String())

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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    looking_hiring_type = db.Column(db.Integer, db.ForeignKey('hiring_type.id'))
    degree = db.Column(db.Integer, db.ForeignKey('degree_type.id'))
    graduating_date = db.Column(db.Date)
    available_date = db.Column(db.Date)
    github_link = db.Column(db.String(255))
    linkedin_link = db.Column(db.String(255))
    portfolio_link = db.Column(db.String(255))
    school_email = db.Column(db.String(255))
    major = db.Column(db.String(50))

    def __repr__(self):
        return f"Student(user_id: '{self.user_id}')"

    @property
    def serialize(self):
        user = User.query.filter_by(id=self.id).first()
        college = College.query.filter_by(id=self.college_id).first()
        college_name = 'None' if not college else college.name
        persuing_degree = Degree.query.filter_by(id=self.degree).first()
        persuing_hiring_type = HiringType.query.filter_by(id=self.looking_hiring_type).first()

        majors = None
        if self.major:
            majors = [major for major in self.major.split(',')]

        return {
            'persuing_work_type': persuing_hiring_type,
            'school_email': self.school_email,
            'portfolio_link': self.portfolio_link,
            'linkedin_link': self.linkedin_link,
            'github_link': self.github_link,
            'available_date': self.available_date,
            'graduating_date': self.graduating_date,
            'major': majors,
            'persuing_degree': persuing_degree,
            'college_name': college_name,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'id': self.id
        }


class College(db.Model):
    __tablename__ = 'college'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    zipcode = db.Column(db.String(5))
    state = db.Column(db.String(2))
    established = db.Column(db.Date)
    website = db.Column(db.String(255))
    logo_url = db.Column(db.String(255), default='default_college.png')

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
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    careerfair_id = db.Column(db.Integer, db.ForeignKey('careerfair.id'), nullable=False)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'))
    visa_type_id = db.Column(db.Integer, db.ForeignKey('visa_type.id'))
    degree_type_id = db.Column(db.Integer, db.ForeignKey('degree_type.id'), nullable=False)
    hiring_type_id = db.Column(db.Integer, db.ForeignKey('hiring_type.id'), nullable=False)
    hiring_majors = db.Column(db.String())
    tables = db.Column(db.String())

    def __repr__(self):
        return f"CareerFairEmployer('{self.hiring_majors}', '{self.employer_id}')"

    @property
    def serialize(self):
        degree = Degree.query.filter_by(id=self.degree_type_id).first()
        hiring_type = HiringType.query.filter_by(id=self.hiring_type_id).first()
        visa = Visa.query.filter_by(id=self.visa_type_id).first()
        employer = Employer.query.filter_by(id=self.employer_id).first()
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
            'careerfair_id': self.careerfair_id,
            '_id': self.id
        }


class CareerFair(db.Model):
    __tablename__ = 'careerfair'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String, nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    zipcode = db.Column(db.String(5))
    other_organization = db.Column(db.String(50))
    map_url = db.Column(db.String())
    employers = db.relationship(CareerFairEmployer, backref='careerfair', lazy=True)

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
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    careerfair_id = db.Column(db.Integer, db.ForeignKey('careerfair.id'))

    def __repr__(self):
        return f"Like('{self.id}')"


class Top5(db.Model):
    __tablename__ = 'top_five_employers'
    id = db.Column(db.Integer, primary_key=True)
    top1 = db.Column(db.Integer, db.ForeignKey('employer.id'))
    top2 = db.Column(db.Integer, db.ForeignKey('employer.id'))
    top3 = db.Column(db.Integer, db.ForeignKey('employer.id'))
    top4 = db.Column(db.Integer, db.ForeignKey('employer.id'))
    top5 = db.Column(db.Integer, db.ForeignKey('employer.id'))
    careerfair_id = db.Column(db.Integer, db.ForeignKey('careerfair.id'))
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Top5('{self.id}')"

    @property
    def serialize(self):
        employer1 = Employer.query.get(self.top1)
        employer2 = Employer.query.get(self.top2)
        employer3 = Employer.query.get(self.top3)
        employer4 = Employer.query.get(self.top4)
        employer5 = Employer.query.get(self.top5)
        careerfair = CareerFair.query.get(self.careerfair_id)

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String())
    hiring_types = db.Column(db.Integer, db.ForeignKey('hiring_type.id'))
    hiring_majors = db.Column(db.String())
    degree = db.Column(db.Integer, db.ForeignKey('degree_type.id'))
    visa = db.Column(db.Integer, db.ForeignKey('visa_type.id'))
    fair_id = db.Column(db.Integer, db.ForeignKey('fair.id'))
    company_url = db.Column(db.String())

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
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    fair_id = db.Column(db.Integer, db.ForeignKey('fair.id'))
    table_number = db.Column(db.Integer)
    fair = db.relationship('Fair')
    company = db.relationship('Company')


class Fair(db.Model):
    # __tablename__ = 'fair'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String)
    organization = db.Column(db.String(250))
    companies = db.relationship('Company', backref='fair', lazy=True)

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
