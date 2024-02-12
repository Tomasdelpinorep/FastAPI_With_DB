from sqlalchemy import Column, Integer, String
from database import Base


class PersonDB(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
