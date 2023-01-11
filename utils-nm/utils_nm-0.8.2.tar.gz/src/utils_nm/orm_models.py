# orm_models.py
# -*- coding: utf-8 -*-

"""
ORM (Object-Relational-Mapping) objects which serve for database purposes
"""

import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute


# ______________________________________________________________________________________________________________________


Base = sa.orm.declarative_base()


class BaseClass:
    """
    Base class which implements general functionality
    """

    @classmethod
    def set_table_attribute(cls, attr_name: str, attr_value: object) -> None:
        """
        sets the attribute for the table, e.g. 'schema' = 'job' or 'name' = 'job_exec'

        Args:
            attr_name: the name of the table attribute
            attr_value: the value to be set for the attribute

        Returns:
            None
        """

        setattr(cls.__table__, attr_name, attr_value)
        return None

    @classmethod
    def create_table(cls, engine: sa.engine.Engine, recreate: bool = False) -> None:
        """
        creates a job execution information table. Only use once!

        Args:
            engine: the sqlalchemy engine to the database
            recreate: if true drop the existing table and recreate it

        Returns:
            Creates the specified table and returns None
        """

        if recreate:
            cls.__table__.drop(engine, checkfirst=True)
        cls.__table__.create(engine, checkfirst=True)

        return None

    @classmethod
    def select_all(cls, engine: sa.engine.Engine) -> list[object]:
        """
        retrieves all rows as orm instances to a list

        Args:
            engine: the sqlalchemy engine used to connect to the database

        Returns:
            list of all object instances
        """
        with Session(engine) as session:
            session.expire_on_commit = False  # keep the instance accessible after session closes
            stmt = sa.select(cls)
            rows = session.execute(stmt).all()
            session.commit()
            rows = [r[0] for r in rows]

        return rows

    @classmethod
    def select_filtered(cls, engine: sa.engine.Engine, verbose: bool = False, **kwargs) -> list[object]:
        """
        retrieves filtered rows as orm instances to a list

        Args:
            engine: the sqlalchemy engine used to connect to the database
            verbose: if true print the generated sql statement
            **kwargs: the key value pairs corresponding to table colum and colum value to filter

        Returns:
            filtered list of object instances
        """
        with Session(engine) as session:
            session.expire_on_commit = False  # keep the instance accessible after session closes
            stmt = sa.select(cls).filter_by(**kwargs)
            if verbose:
                print(stmt)
            rows = session.execute(stmt).all()
            session.commit()
            rows = [r[0] for r in rows]

        return rows

    def add(self, engine: sa.engine.Engine) -> object:
        """
        writes the current instance to the database

        Args:
            engine: the sqlalchemy engine used to connect to the database

        Returns:
            self
        """

        with Session(engine) as session:
            session.expire_on_commit = False  # keep the instance accessible after session closes
            if self.id is None:
                session.add(self)
            session.commit()
        return self

    def update(self, engine: sa.engine.Engine) -> None:
        """
       updates the current instance to the database

        Args:
            engine: the sqlalchemy engine used to connect to the database

        Returns:
            None
        """

        with Session(engine) as session:
            session.expire_on_commit = False  # keep the instance accessible after session closes
            mapped_values = {}
            primary_keys = [element.name for element in self.__class__.__table__.primary_key]
            for key, value in self.__class__.__dict__.items():
                if isinstance(value, InstrumentedAttribute) and key not in primary_keys:
                    mapped_values[key] = getattr(self, key)

            session.query(self.__class__).filter(self.__class__.id == self.id).update(mapped_values)
            session.commit()
        return None


# ______________________________________________________________________________________________________________________


class JobExec(Base, BaseClass):
    """
    ORM model for the job_execution table
    """

    __tablename__ = 'job_execution'
    __table_args__ = {'schema': None}

    id = sa.Column(sa.Integer, sa.Identity(start=1, cycle=True), primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    start_time = sa.Column(sa.DateTime, nullable=False)
    end_time = sa.Column(sa.DateTime, nullable=True)
    status = sa.Column(sa.String(255), nullable=True)
    running = sa.Column(sa.Boolean, nullable=False)
    executor = sa.Column(sa.String(31), nullable=False)
    exception = sa.Column(sa.String(255), nullable=True)
    log_file = sa.Column(sa.String(255), nullable=True)

    def __repr__(self):
        return f'JobExec(id={self.id}, name={self.name}, start_time={self.start_time}, status={self.status})'


# ______________________________________________________________________________________________________________________


class JobSchedule(Base, BaseClass):
    """
    ORM model for the job_schedule table
    """

    __tablename__ = 'job_schedule'
    __table_args__ = {'schema': None}

    id = sa.Column(sa.Integer, sa.Identity(start=1, cycle=True), primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    location = sa.Column(sa.String(255), nullable=False)
    args = sa.Column(sa.String(255), nullable=False)
    env = sa.Column(sa.String(255), nullable=False)
    schedule = sa.Column(sa.String(255), nullable=False)
    priority = sa.Column(sa.SmallInteger, nullable=True)
    active = sa.Column(sa.Boolean, default=True, nullable=False)

    def __repr__(self):
        schedule = zip(self.schedule.split(), ['minute', 'hour', 'day', 'month', 'weekday'])
        schedule = ', '.join([f'{j}={i}' for i, j in schedule])
        return f'JobSchedule(id={self.id}, name={self.name}, args={self.args}, schedule=[{schedule}])'


# ______________________________________________________________________________________________________________________
