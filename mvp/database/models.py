from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Table, Boolean, Numeric
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Bridge table: Links Persons to Cases
person_cases = Table(
    'person_cases', Base.metadata,
    Column('person_id', Integer, ForeignKey('persons.person_id'), primary_key=True),
    Column('case_id', Integer, ForeignKey('cases.case_id'), primary_key=True),
    Column('role', String, default='Suspect')
)

class Person(Base):
    __tablename__ = 'persons'
    person_id = Column(Integer, primary_key=True)
    
    # Identification & Verification
    national_id_number = Column(String, unique=True)
    nin_verified = Column(Boolean, default=False)
    bvn = Column(String)
    
    # Names
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_names = Column(String)
    
    # Biographic (Nigerian Context)
    date_of_birth = Column(Date)
    gender = Column(String)
    state_of_origin = Column(String)
    lga = Column(String)
    
    # Physicals (Intelligence Layer)
    height_cm = Column(Integer)
    distinguishing_marks = Column(Text) 
    photo_path = Column(String)
    
    # Audit & Soft Delete
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    # Relationships
    aliases = relationship("PersonAlias", back_populates="person")
    contacts = relationship("PersonContact", back_populates="person")
    cases = relationship("Case", secondary=person_cases, back_populates="subjects")

class Case(Base):
    __tablename__ = 'cases'
    case_id = Column(Integer, primary_key=True)
    formation_id = Column(Integer, nullable=False) # Which state owns this
    case_number = Column(String, unique=True, nullable=False)
    offense_type = Column(String)
    description = Column(Text)
    
    # Location
    arrest_address = Column(Text)
    arrest_latitude = Column(Numeric(10, 8))
    arrest_longitude = Column(Numeric(11, 8))
    
    current_status = Column(String, default='Open')
    opened_at = Column(DateTime, default=datetime.utcnow)
    arresting_officer_id = Column(Integer, nullable=False)

    subjects = relationship("Person", secondary=person_cases, back_populates="cases")

class PersonAlias(Base):
    __tablename__ = 'person_aliases'
    alias_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.person_id'))
    alias_name = Column(String, nullable=False)
    alias_type = Column(String) 
    person = relationship("Person", back_populates="aliases")

class PersonContact(Base):
    __tablename__ = 'person_contacts'
    contact_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.person_id'))
    contact_type = Column(String) 
    contact_value = Column(Text, nullable=False)
    person = relationship("Person", back_populates="contacts")