from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time
from sqlalchemy.orm import relationship
import json
import os,sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

with open('{}/config.json'.format(current_dir), 'r') as f:
    config = json.load(f)
postgres = config["POSTGRES"]
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    kind = Column(Integer)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
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
    organization = Column(String(250), nullable=False)
    companies = relationship('Company')

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        comapnies = [company.serialize for company in self.companies]
        return {
            'id': self.id,
            'name': self.name,
            'organization': self.organization,
            'description': self.description,
            'companies': comapnies,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'start_time': self.start_time,
            'end_time': self.end_time
        }


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
    fair = relationship(Fair)

    @property
    def serialize(self):
        """
        Return object data in easily serializable format

        hiring types:
        1: intern
        2: full time
        3: intern + full time

        degree:
        1: BS
        2: MS
        3: PhD
        4: BS, MS
        5: BS, PhD
        6: MS, PhD
        7: BS, MS, PhD

        visa:
        1: false
        2: true
        3: maybe
        """

        degree = ['BS', 'MS', 'PhD', ['BS', 'MS'], ['BS', 'PhD'],
                  ['MS', 'PhD'], ['BS', 'MS' 'PhD']]

        types = ['INT', 'FT', ['INT', 'FT']]
        visa = ['yes', 'no', 'maybe']
        majors = [major.strip() for major in self.hiring_majors.split(',')]

        return {
            'fair': self.fair,
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
"""
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
                                                postgres["user"],
                                                postgres["pw"],
                                                postgres["endpoint"],
                                                postgres["port"],
                                                postgres["db"]))

"""
engine = create_engine('sqlite:///careertalk.db')
Base.metadata.create_all(engine)
