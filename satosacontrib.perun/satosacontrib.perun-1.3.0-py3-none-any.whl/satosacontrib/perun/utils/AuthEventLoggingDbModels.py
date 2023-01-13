from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
)
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AuthEventLoggingTable(Base):
    __tablename__ = "auth_event_logging"

    id = Column(Integer, primary_key=True)
    day = Column(DATETIME2)
    user = Column(String)
    idp_id = Column(Integer, ForeignKey("logging_idp.id"))
    sp_id = Column(Integer, ForeignKey("logging_sp_id.id"))
    ip_address = Column(String)
    geolocation_city = Column(String)
    geolocation_country = Column(String)
    session_id = Column(Integer, ForeignKey("session_id_values.id"))
    requested_acrs_id = Column(Integer, ForeignKey("requested_acrs_values.id"))
    upstream_acrs_id = Column(Integer, ForeignKey("upstream_acrs_values.id"))
    user_agent_raw_id = Column(Integer, ForeignKey("user_agent_raw_values.id"))
    user_agent_id = Column(Integer, ForeignKey("user_agent_values.id"))


class LoggingIdpTable(Base):
    __tablename__ = "logging_idp"

    id = Column(Integer, primary_key=True)
    identifier = Column(String)
    name = Column(String)


class LoggingSpTable(Base):
    __tablename__ = "logging_sp"

    id = Column(Integer, primary_key=True)
    identifier = Column(String)
    name = Column(String)


class SessionIdTable(Base):
    __tablename__ = "session_id_values"

    id = Column(Integer, primary_key=True)
    value = Column(String)


class RequestedAcrsTable(Base):
    __tablename__ = "requested_acrs_values"

    id = Column(Integer, primary_key=True)
    value = Column(String)


class UpstreamAcrsTable(Base):
    __tablename__ = "upstream_acrs_values"

    id = Column(Integer, primary_key=True)
    value = Column(String)


class UserAgentRawTable(Base):
    __tablename__ = "user_agent_raw_values"

    id = Column(Integer, primary_key=True)
    value = Column(String)


class UserAgentTable(Base):
    __tablename__ = "user_agent_values"

    id = Column(Integer, primary_key=True)
    value = Column(String)
