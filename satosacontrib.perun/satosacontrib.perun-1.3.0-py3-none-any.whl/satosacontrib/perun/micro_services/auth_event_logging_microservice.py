import json
import logging
import satosa.logging_util as lu

from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
from user_agents import parse
from satosa.micro_services.base import ResponseMicroService
from geoip2 import database
from satosacontrib.perun.utils.AuthEventLoggingDbModels import (
    Base,
    AuthEventLoggingTable,
    LoggingIdpTable,
    LoggingSpTable,
    SessionIdTable,
    RequestedAcrsTable,
    UpstreamAcrsTable,
    UserAgentTable,
    UserAgentRawTable,
)
from sqlalchemy import select, create_engine

logger = logging.getLogger(__name__)


# noinspection SpellCheckingInspection
class AuthEventLogging(ResponseMicroService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id_attr = config.get("user_identifier_attr", None)
        self.logging_db = config["logging_db"]
        self.geolite_file_path = config["path_to_geolite2_city"]
        self.ip_address_header = config.get("ip_address_header", "REMOTE_ADDR")
        logger.info("AuthEventLogging is active")

    @staticmethod
    def __get_id_from_identifier(cnxn, metadata, identifier, name, table):
        metadata.create_all(cnxn)

        insert_stmt = insert(table).values(None, identifier, name)
        if name is None or name == "":
            insert_stmt = insert_stmt.on_conflict_do_nothing()
        else:
            insert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=["identifier"], set_=dict(name=name)
            )

        cnxn.execute(insert_stmt)

        result = select(getattr(table.columns, "id")).where(
            table.columns.identifier == identifier
        )
        return result.scalar()

    @staticmethod
    def __get_id_from_foreign_table(cnxn, metadata, value, table):
        metadata.create_all(cnxn)

        insert_stmt = insert(table).values([None, value])
        if value is None or value == "":
            insert_stmt = insert_stmt.on_conflict_do_nothing()
        else:
            insert_stmt = insert_stmt.on_conflict_do_update(set_=dict(value=value))

        cnxn.execute(insert_stmt)

        result = select(getattr(table.columns, "id")).where(
            table.columns.value == value
        )
        return result.scalar()

    def __get_location(self, ip):
        with database.Reader(self.geolite_file_path) as reader:
            response = reader.city(ip)

            return {"city": response.city.name, "country": response.country.name}

    def process(self, context, data):
        idp = data.auth_info["issuer"]
        sp = data.requester
        sp_name = data.requester_name[0]["text"] or ""
        user = data[self.user_id_attr] if self.user_id_attr else data.subject_id
        ip_address = context.http_headers[self.ip_address_header]
        geolocation = self.__get_location(ip_address)
        geolocation_city = geolocation.get("city", None)
        geolocation_country = geolocation.get("country", None)
        session_id = lu.get_session_id(context.state)
        requested_acrs = context.state.get(
            context.KEY_AUTHN_CONTEXT_CLASS_REF
        ) or context.get_decoration(context.KEY_AUTHN_CONTEXT_CLASS_REF)
        upstream_acrs = data.auth_info["auth_class_ref"]
        user_agent_raw = context.http_headers.get("User-Agent")
        user_agent_parsed = json.dumps(str(parse(user_agent_raw)))

        engine = create_engine(self.logging_db)
        cnxn = engine.connect()
        metadata = Base.metadata
        metadata.bind = cnxn
        auth_event_logging = AuthEventLoggingTable().__table__

        metadata.create_all(engine)

        idp_id = self.__get_id_from_identifier(
            cnxn, metadata, idp, "", LoggingIdpTable().__table__
        )
        sp_id = self.__get_id_from_identifier(
            cnxn, metadata, sp, sp_name, LoggingSpTable().__table__
        )
        session_id_values_id = self.__get_id_from_foreign_table(
            cnxn, metadata, session_id, SessionIdTable().__table__
        )
        requested_acrs_id = self.__get_id_from_foreign_table(
            cnxn, metadata, requested_acrs, RequestedAcrsTable().__table__
        )
        upstream_acrs_id = self.__get_id_from_foreign_table(
            cnxn, metadata, upstream_acrs, UpstreamAcrsTable().__table__
        )
        user_agent_raw_id = self.__get_id_from_foreign_table(
            cnxn, metadata, user_agent_raw, UserAgentRawTable().__table__
        )
        user_agent_id = self.__get_id_from_foreign_table(
            cnxn, metadata, user_agent_parsed, UserAgentTable().__table__
        )

        fields = {
            "id": None,
            "day": datetime.utcnow(),
            "user": user,
            "idp_id": idp_id,
            "sp_id": sp_id,
            "ip_address": ip_address,
            "geolocation_city": geolocation_city,
            "geolocation_country": geolocation_country,
            "session_id": session_id_values_id,
            "requested_acrs_id": requested_acrs_id,
            "upstream_acrs_id": upstream_acrs_id,
            "user_agent_raw_id": user_agent_raw_id,
            "user_agent_id": user_agent_id,
        }

        insert_stmt = insert(auth_event_logging).values(**fields)
        cnxn.execute(insert_stmt)

        return super().process(context, data)
