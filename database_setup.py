from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time
from sqlalchemy.orm import relationship, sessionmaker
import json
import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

with open('{}/config.json'.format(current_dir), 'r') as f:
    config = json.load(f)

postgres = config["POSTGRES"]
Base = declarative_base()


engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
                                                postgres["user"],
                                                postgres["pw"],
                                                postgres["endpoint"],
                                                postgres["port"],
                                                postgres["db"]),
                                            connect_args={'sslmode':'require'})


#engine = create_engine('sqlite:///careertalk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


def _to_minutes(time):
    t = time.hour * 60 + time.minute
    return t


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    kind = Column(Integer)
    picture = Column(String(250))
    resume = Column(String(250))
    bio = Column(String(250))


    def serialize(self):
        type = ['student','faculty', 'corporate']
        return {
            'id': self.id,
            'name': self.name,
            'kind': type[self.kind],
            'bio': self.bio,
            'resume': self.resume,
            'picture': self.picture,
            'start_date': self.start_date
        }


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
    organization = Column(String(250), nullable=False)
    companies = relationship('Company')

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


# class Favorite(Base):
#     __tablename__ = 'favorite_company'
#     id = Column(Integer, primary_key=True)
#     company_id = Column(Integer, ForeignKey('company_id'))
#     user_id = Column(Integer, ForeignKey('user_id'))
#     fair_id = Column(Integer, ForeignKey('fair_id'))


class HiringType(Base):
    __tablename__ = 'hiring_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)


class Degree(Base):
    __tablename__ = 'degree_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)


class Visa(Base):
    __tablename__ = 'visa_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(6), nullable=False)



Base.metadata.create_all(engine)
