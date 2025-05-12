from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()
# this is the base class which is used to define the actual table
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    gmail = Column(String(100), nullable=False)
    


# base.metadata is a schema that manages the tables and columns