import logging

from influxdb import InfluxDBClient


class InfluxClient:
    def __init__(self, influxdb_database: str, influxdb_ip: str, influxdb_port: int = 8086, influxdb_protocol="http", logger: logging.Logger = None):
        valid_protocols = ("http", "https")
        if influxdb_protocol not in valid_protocols:
            raise ValueError(f"{influxdb_protocol} is invalid; choose one of {valid_protocols}")

        self.client = InfluxDBClient(influxdb_ip, influxdb_port, database=influxdb_database)
        self.database = influxdb_database
        self.ip = influxdb_ip
        self.port = influxdb_port
        self.protocol = influxdb_protocol
        self.logger = logger

    @property
    def database(self):
        return self.influxdb_database

    @database.setter
    def database(self, v):
        self.influxdb_database = v

    @property
    def ip(self):
        return self.influxdb_ip

    @ip.setter
    def ip(self, v):
        self.influxdb_ip = v

    @property
    def port(self):
        return self.influxdb_port

    @port.setter
    def port(self, v):
        self.influxdb_port = v

    @property
    def protocol(self):
        return self.influxdb_protocol

    @protocol.setter
    def protocol(self, v):
        self.influxdb_protocol = v

    def log(self, msg, level: int = logging.DEBUG):
        if self.logger:
            self.logger.log(level, msg)
