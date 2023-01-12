"""Manage GDN collection streams"""

import json
import logging

import pulsar
import singer
from c8 import C8Client
from singer import utils
from singer.catalog import CatalogEntry


class GDNCollectionClient:
    """Client for handling GDN collection streams."""

    def __init__(self, config) -> None:
        """Init new GDN Collection Client."""
        _host = config.get("region")
        _fabric = config.get("fabric")
        _apikey = config.get("api_key")
        self._collection = config.get("source_collection")
        self._c8_client = C8Client(
            "https",
            host=_host,
            port=443,
            geofabric=_fabric,
            apikey=_apikey
        )
        _auth = pulsar.AuthenticationToken(_apikey)
        _tenant = self._c8_client.tenant(apikey=_apikey).tenant_name

        # enable collection stream on the source collection.
        self._c8_client.update_collection_properties(self._collection, has_stream=True)

        # pulsar client throws some messages into stdout when subscribed to a topic. Meltano tap/target doesn't like
        # this and tries to process the pulsar log messages in stdout as input singer records. Therefore we are trying
        #  to turn off pulsar logging here. This is the best way I found with the current pulsar client API.
        _pulsar_logger = logging.getLogger("pulsar-logger")
        _pulsar_logger.setLevel(logging.CRITICAL)
        _pulsar_logger.addHandler(logging.NullHandler())

        _pulsar_client = pulsar.Client(
            f"pulsar+ssl://{_host}:6651/",
            authentication=_auth,
            tls_allow_insecure_connection=False,
            logger=_pulsar_logger,
        )
        _sub_name = f"collection_source_{_tenant}.{_fabric}_{self._collection}"
        _topic = f"persistent://{_tenant}/c8local.{_fabric}/{self._collection}"
        self._consumer: pulsar.Consumer = _pulsar_client.subscribe(_topic, _sub_name)

    def sync(self, stream):
        """Return documents in target GDN collection as records."""
        if self._c8_client.has_collection(self._collection):
            self.send_schema_message(stream)
            self.load_existing_data(stream)
            meta_keys = ['_key', '_rev', '_sdc_deleted_at']
            while True:
                msg = self._consumer.receive()
                data = msg.data()
                if data == None or not data:
                    continue
                props = msg.properties()
                j = json.loads(data.decode("utf8"))
                j['_sdc_deleted_at'] = None
                if props["op"] == "INSERT" or props["op"] == "UPDATE":
                    # skip inserts without data.
                    if len(j.keys() ^ meta_keys) > 0:
                        singer_record = self.msg_to_singer_message(stream, j, None, utils.now())
                        singer.write_message(singer_record)
                elif props["op"] == "DELETE":
                    j['_sdc_deleted_at'] = singer.utils.strftime(utils.now())
                    singer_record = self.msg_to_singer_message(stream, j, None, utils.now())
                    singer.write_message(singer_record)
                self._consumer.acknowledge(msg.message_id())
        else:
            raise FileNotFoundError("Collection {} not found".format(self._collection))

    def load_existing_data(self, stream):
        cursor = self._c8_client.execute_query(f"FOR d IN @@collection RETURN d",
                                               bind_vars={"@collection": self._collection})
        while (not cursor.empty()) or cursor.has_more():
            rec = cursor.next()
            singer_record = self.msg_to_singer_message(stream, rec, None, utils.now())
            singer.write_message(singer_record)

    def send_schema_message(self, stream: CatalogEntry, bookmark_properties=[]):
        schema_message = singer.SchemaMessage(stream=stream.stream,
                                              schema=stream.schema.to_dict(),
                                              key_properties=stream.key_properties,
                                              bookmark_properties=bookmark_properties)
        singer.write_message(schema_message)

    def msg_to_singer_message(self, stream, msg, version, time_extracted):
        return singer.RecordMessage(
            stream=stream.stream,
            record=msg,
            version=version,
            time_extracted=time_extracted
        )
