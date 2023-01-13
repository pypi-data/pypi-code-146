from datetime import datetime

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings


class InfluxDbWriter:
    def __init__(
        self,
        url,
        token,
        org,
        bucket="",
        measurement="",
    ):
        """
        Generate InfluxDbWriter

        :param url: InfluxDB URL
        :param token: API Token. You can generate an API token from the
            "API Tokens Tab" in the UI
        :param org: Organisation name

        :param bucket: Bucket name - default is ""
        """
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        self.measurement = measurement

    def write_data(self, data, tags, time=None, bucket=None, measurement=None):
        """
        Write data to an InfluxDB

        :param data: Data as dict. Can contain multiple key value pairs, i.e.:
            {"num_butterflies": 4, "num_dragonflies": 13}
        :param tags: Tags as dict. Can contain multiple key value pairs, i.e.:
            {"location": "KA", "scientist": "Humbold"}
        :param time: Timestamp.
            If none is given, the current UTC time is used!
            - default is None
        :param bucket: Bucket name.
            If given this overrides the instance bucket name!
            - default is None
        :param measurement: Measurement name.
            If given this overrides the instance measurement!
            - default is None
        """
        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)

            measurement = measurement if measurement else self.measurement
            point = Point(measurement)

            for tag, value in tags.items():
                point.tag(tag, value)

            for key, value in data.items():
                point.field(key, value)

            time = time if time else datetime.utcnow()

            point.time(time=time)

            bucket = bucket if bucket else self.bucket

            write_api.write(bucket, self.org, point)

    def write_df(
        self, df, static_tags=None, bucket=None, measurement=None, tag_columns=None
    ):
        """Write dataframe to InfluxDB

        Args:
            df (Pandas DataFrame with datetime index):
                dataframe to write, columns will be written as fields
            static_tags (Dict): dict with static tags
            bucket (String): bucket
            measurement (String): measurement
            tag_columns (list): list of columns to use as tags
        """
        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:
            if static_tags:
                point_settings = PointSettings(**static_tags)
            else:
                point_settings = None

            write_api = client.write_api(
                write_options=SYNCHRONOUS, point_settings=point_settings
            )

            measurement = measurement if measurement else self.measurement
            bucket = bucket if bucket else self.bucket

            write_api.write(
                bucket=bucket,
                record=df,
                data_frame_measurement_name=measurement,
                data_frame_tag_columns=tag_columns,
            )
