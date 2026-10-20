from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Numeric, func
from sqlalchemy.orm import relationship, declarative_base

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Numeric, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'
    
    person_id = Column(Integer, primary_key=True)
    
    # --- Identity ---
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_names = Column(Text)
    date_of_birth = Column(String)  # ISO format recommended: YYYY-MM-DD
    gender = Column(String)
    aliases = Column(Text)
    # --- Heritage & Verification ---
    nationality = Column(String, default="Nigerian")
    state_of_origin = Column(String)
    lga = Column(String)
    fathers_name = Column(Text)
    mothers_name = Column(Text)
    mothers_maiden_name = Column(Text)
    
    # --- Identification (Unique & Indexed) ---
    national_id_number = Column(String, unique=True, index=True)
    nin_verified = Column(Boolean, default=False)
    bvn = Column(String, index=True)
        
    # --- Physicals & Intelligence ---
    height_cm = Column(Integer)
    distinguishing_marks = Column(Text) 
    
    # --- System Metadata ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False, index=True)

    # --- Relationships ---
    # Using 'delete-orphan' ensures that if a Person is deleted, their sub-data is cleaned up
    aliases = relationship("PersonAlias", back_populates="person", cascade="all, delete-orphan")
    contacts = relationship("PersonContact", back_populates="person", cascade="all, delete-orphan")
    biometrics = relationship("Biometric", back_populates="person", cascade="all, delete-orphan")
    affiliations = relationship("PersonAffiliation", back_populates="person", cascade="all, delete-orphan")
    
    # Link to Cases through the PersonCase association object
    cases = relationship("PersonCase", back_populates="person")

class Biometric(Base):
    __tablename__ = 'biometrics'

    biometric_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.person_id'), nullable=False)
    biometric_type = Column(String, default="photo")  # 'photo', 'fingerprint'
    file_path = Column(String, nullable=False)        # Local path to assets/photos/
    captured_at = Column(DateTime(timezone=True), server_default=func.now())
    
    person = relationship("Person", back_populates="biometrics")

class Case(Base):
    __tablename__ = 'cases'
    
    case_id = Column(Integer, primary_key=True)
    formation_id = Column(Integer, nullable=False)   # Command/State reference
    case_number = Column(String, unique=True, nullable=False, index=True)
    offense_type = Column(String)
    description = Column(Text)
    
    # Location Intelligence
    arrest_date = Column (DateTime)
    arrest_address = Column(Text)
    arrest_latitude = Column(Numeric(10, 8))
    arrest_longitude = Column(Numeric(11, 8))
    
    current_status = Column(String, default='Open')
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    arresting_officer_id = Column(Integer, nullable=False)

    # Relationship to subjects
    subjects = relationship("PersonCase", back_populates="case")

class PersonCase(Base):
    """Association Class for many-to-many relationship with extra data (role)"""
    __tablename__ = 'person_cases'
    
    person_id = Column(Integer, ForeignKey('persons.person_id'), primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.case_id'), primary_key=True)
    role = Column(String, default='Suspect') # Suspect, Witness, Accomplice
    
    person = relationship("Person", back_populates="cases")
    case = relationship("Case", back_populates="subjects")

class PersonAlias(Base):
    __tablename__ = 'person_aliases'
    alias_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.person_id'), nullable=False)
    alias_name = Column(String, nullable=False)
    alias_type = Column(String)  # 'Street name', 'Legal Alias'
    
    person = relationship("Person", back_populates="aliases")

class PersonContact(Base):
    __tablename__ = 'person_contacts'
    contact_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.person_id'), nullable=False)
    contact_type = Column(String) # 'Phone', 'Email', 'WhatsApp'
    contact_value = Column(Text, nullable=False)
    
    person = relationship("Person", back_populates="contacts")

class Organization(Base):
    __tablename__ = 'organizations'
    org_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    org_type = Column(String) # 'School', 'Cult', 'NGO'
    
    members = relationship("PersonAffiliation", back_populates="organization")

class PersonAffiliation(Base):
    __tablename__ = 'person_affiliations'
    affiliation_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.person_id'), nullable=False)
    org_id = Column(Integer, ForeignKey('organizations.org_id'), nullable=False)
    role = Column(String) # 'Leader', 'Member', 'Recruiter'
    is_active = Column(Boolean, default=True)

    person = relationship("Person", back_populates="affiliations")
    organization = relationship("Organization", back_populates="members")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user") # "admin" or "user"
    is_active = Column(Boolean, default=True)

class SystemMetadata(Base):
    __tablename__ = "system_metadata"
    id = Column(Integer, primary_key=True)
    version = Column(String, default="1.0.0")
    last_updated = Column(DateTime, default=func.now())