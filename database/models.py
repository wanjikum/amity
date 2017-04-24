from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RoomModel(Base):
    """Defines the room table"""
    __tablename__ = "rooms"
    room_id = Column(Integer, primary_key=True)
    room_name = Column(String(50), unique=True, nullable=False)
    room_type = Column(String(50), nullable=False)
    room_capacity = Column(Integer(), nullable=False)
    occupants = Column(String(200))


class PersonModel(Base):
    """Defines the person table"""
    __tablename__ = "people"
    person_id = Column(String, primary_key=True)
    person_name = Column(String, nullable=False)
    person_type = Column(String(50), nullable=False)
    office_allocated = Column(String(50), nullable=True)
    livingspace_allocated = Column(String(50), nullable=True)
    wants_accomodation = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
