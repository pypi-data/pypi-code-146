#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Text

from slpkg.configs import Configs


DATABASE_URI = os.path.join(f'sqlite:///{Configs.db_path}', Configs.database)

engine = create_engine(DATABASE_URI)

session = sessionmaker(engine)()
Base = declarative_base()


@dataclass
class SBoTable(Base):
    """ The main table for the SBo repository. """

    __tablename__ = 'sbotable'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(Text)
    location: str = Column(Text)
    files: str = Column(Text)
    version: str = Column(Text)
    download: str = Column(Text)
    download64: str = Column(Text)
    md5sum: str = Column(Text)
    md5sum64: str = Column(Text)
    requires: str = Column(Text)
    short_description: str = Column(Text)


@dataclass
class LogsDependencies(Base):
    """ The table that stores the dependencies after installing a package. """

    __tablename__ = 'logsdependencies'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(Text)
    requires: str = Column(Text)


Base.metadata.create_all(engine)
