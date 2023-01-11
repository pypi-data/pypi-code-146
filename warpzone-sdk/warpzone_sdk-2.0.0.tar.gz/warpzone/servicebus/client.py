""" Module w.r.t. Azure service bus logic."""

import base64 as b64
from functools import reduce
from typing import Iterator

import pandas as pd
import pyarrow as pa
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from warpzone.transform import data


class WarpzoneSubscriptionClient:
    """Class to interact with Azure Service Bus Topic Subscription"""

    def __init__(
        self,
        service_bus_client: ServiceBusClient,
        topic_name: str,
        subscription_name: str,
    ):
        self._service_bus_client = service_bus_client
        self.topic_name = topic_name
        self.subscription_name = subscription_name

    @classmethod
    def from_connection_string(
        cls, conn_str: str, topic_name: str, subscription_name: str
    ) -> "WarpzoneSubscriptionClient":
        """Get subscription client from connection string

        Args:
            conn_str (str): Connection string to Service Bus
            topic_name (str): Name of topic
            subscription_name (str): Name of subscription
        """
        service_bus_client = ServiceBusClient.from_connection_string(conn_str)
        return cls(service_bus_client, topic_name, subscription_name)

    def _get_subscription_receiver(self, max_wait_time: int = None):
        return self._service_bus_client.get_subscription_receiver(
            self.topic_name, self.subscription_name, max_wait_time=max_wait_time
        )

    def receive_data(
        self, max_wait_time: int = None, decode_b64: bool = True
    ) -> Iterator[bytes]:
        """Receive data from the service bus topic subscription.

        Args:
            max_wait_time (int, optional):
                The timeout in seconds between received messages after which
                the receiver will automatically stop receiving.
                The default value is None, in which case there is no timeout at all.
            decode_b64 (bool, optional): Base 64 decode data. Defaults to True.

        Yields:
            Iterator[bytes]: Received data
        """
        with self._get_subscription_receiver(max_wait_time) as receiver:
            for msg in receiver:
                msg_body_parts = msg.message.get_data()
                # message data can either be a generator
                # of string or bytes. We want to concatenate
                # them in either case
                msg_body = reduce(lambda x, y: x + y, msg_body_parts)
                if decode_b64:
                    msg_body = b64.b64decode(msg_body)
                yield msg_body

    def receive_arrow(self, max_wait_time: int = None) -> Iterator[pa.Table]:
        """Receive arrow tables from the service bus topic subscription from parquet.

        Args:
            max_wait_time (int, optional):
                The timeout in seconds between received messages after which
                the receiver will automatically stop receiving.
                The default value is None, in which case there is no timeout at all.

        Yields:
            Iterator[pa.Table]: Received arrow tables
        """
        for msg_body in self.receive_data(max_wait_time):
            yield data.parquet_to_arrow(msg_body)

    def receive_pandas(self, max_wait_time: int = None) -> Iterator[pd.DataFrame]:
        """Receive pandas dataframes from the service bus topic subscription from
        parquet.

        Args:
            max_wait_time (int, optional):
                The timeout in seconds between received messages after which
                the receiver will automatically stop receiving.
                The default value is None, in which case there is no timeout at all.

        Yields:
            Iterator[pd.DataFrame]: Received pandas dataframes.
        """
        for msg_body in self.receive_data(max_wait_time):
            yield data.parquet_to_pandas(msg_body)


class WarpzoneTopicClient:
    """Class to interact with Azure Service Bus Topic"""

    def __init__(self, service_bus_client: ServiceBusClient, topic_name: str):
        self._service_bus_client = service_bus_client
        self.topic_name = topic_name

    @classmethod
    def from_connection_string(
        cls, conn_str: str, topic_name: str
    ) -> "WarpzoneTopicClient":
        """Get topic client from connection string

        Args:
            conn_str (str): Connection string to service bus
            topic_name (str): Name of topic
        """
        service_bus_client = ServiceBusClient.from_connection_string(conn_str)
        return WarpzoneTopicClient(service_bus_client, topic_name)

    def _get_topic_sender(self):
        return self._service_bus_client.get_topic_sender(self.topic_name)

    def send_data(
        self,
        content: bytes,
        subject: str,
        user_properties: dict = {},
        encode_b64: bool = True,
    ):
        """Send data to the service bus topic.

        Args:
            content (Union[str, bytes]): The content of the message.
            subject (str): The subject of the message.
            user_properties (dict, optional): Custom user properties. Defaults to {}.
            encode_b64 (bool, optional): Base 64 encode data. Defaults to True.
        """

        if encode_b64:
            content = b64.b64encode(content)

        msg = ServiceBusMessage(
            body=content,
            subject=subject,
            application_properties=user_properties,
        )

        with self._get_topic_sender() as sender:
            sender.send_messages(msg)

    def send_arrow(self, table: pa.Table, subject: str, user_properties: dict = {}):
        """Send arrow table to service bus topic as parquet.

        Args:
            table (pa.Table): Arrow table
            subject (str): The subject of the message
            user_properties (dict, optional): Custom user properties. Defaults to {}.
        """
        msg_body = data.arrow_to_parquet(table)
        self.send_data(msg_body, subject, user_properties)

    def send_pandas(
        self,
        df: pd.DataFrame,
        subject: str,
        user_properties: dict = {},
        schema: dict = None,
    ):
        """Send pandas dataframe to service bus topic as parquet

        Args:
            df (pd.DataFrame): Pandas dataframe
            subject (str): The subject of the message
            user_properties (dict, optional): Custom user properties. Defaults to {}.
            schema (dict, optional): Dictonary of column names and data types to use
                when converting to parquet. Defaults to None, in which case data types
                will automatically be inferred.
        """
        msg_body = data.pandas_to_parquet(df, schema)
        self.send_data(msg_body, subject, user_properties)
