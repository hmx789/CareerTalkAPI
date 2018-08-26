from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
import json

with open('config.json', 'r') as f:
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
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
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
        }


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(), nullable=False)
    hiring_types = Column(Integer)
    hiring_majors = Column(String())
    degree = Column(Integer)
    visa = Column(Integer)
    fair_id = Column(Integer, ForeignKey('fair.id'))
    fair = relationship(Fair)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""

        return {
            'fair': self.fair,
            'fair_id': self.fair_id,
            'visa': self.visa,
            'degree': self.degree,
            'hiring_majors': self.hiring_majors,
            'hiring_types': self.hiring_types,
            'description': self.description,
            'name': self.name,
            'id': self.id,
        }

engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
                                                postgres["user"],
                                                postgres["pw"],
                                                postgres["endpoint"],
                                                postgres["port"],
                                                postgres["db"]))
Base.metadata.create_all(engine)
