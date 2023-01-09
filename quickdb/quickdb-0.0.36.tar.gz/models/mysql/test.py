# coding: utf-8
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    name = Column(VARCHAR(255), primary_key=True, unique=True)
    age = Column(Integer)
    alive = Column(Integer)
