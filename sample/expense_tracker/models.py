from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    category = Column(String)
    amount = Column(Integer)
