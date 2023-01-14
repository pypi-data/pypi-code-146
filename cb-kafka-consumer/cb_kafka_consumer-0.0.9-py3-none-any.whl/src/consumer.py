import json
import logging
from json import JSONDecodeError
from queue import PriorityQueue
from typing import Callable, Any, Union

from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata


class Message:
    def __init__(self, offset: int, topic: str, partition: int, msg: dict):
        self.__offset = offset
        self.__topic = topic
        self.__partition = partition
        self.msg = msg

    def get_offset(self):
        return self.__offset

    def get_topic(self):
        return self.__topic

    def get_partition(self):
        return self.__partition


class CBKafkaConsumer:
    def __init__(self,
                 servers: Union[str, list],
                 consumer_group_id: str,
                 topics: str,
                 callback: Callable[[Message], Any],
                 session_timeout: int = 10000,
                 timeout: int = 1000,
                 batch_size: int = 20,
                 auto_commit: bool = False):
        self.__callback = callback
        self.__batch_size = batch_size
        self.__handled_messages = PriorityQueue(maxsize=0)
        self.__auto_commit = auto_commit

        self.__kafka_consumer = KafkaConsumer(
            topics,
            group_id=consumer_group_id,
            bootstrap_servers=servers,
            session_timeout_ms=session_timeout,
            consumer_timeout_ms=timeout,
            enable_auto_commit=auto_commit,
            auto_offset_reset='earliest'
        )

    def start(self):
        for batch in self.__read_batch():
            [self.__callback(Message(entry[0], entry[1], entry[2], entry[3])) for entry in batch]
            if self.__auto_commit:
                self.__kafka_consumer.commit_async()

    def commit(self, msg: Message):
        if not self.__auto_commit:
            self.__handled_messages.put((msg.get_offset(), msg))
            if self.__handled_messages.qsize() > self.__batch_size:
                prev_msg = self.__handled_messages.get()[1]
                all_ok = True
                for _ in range(self.__batch_size):
                    curr_msg = self.__handled_messages.get()[1]
                    if curr_msg.get_offset() > prev_msg.get_offset() + 1:
                        all_ok = False
                        self.__commit_since_offset(prev_msg)
                        self.__handled_messages.put((prev_msg.get_offset(), prev_msg))
                        self.__handled_messages.put((curr_msg.get_offset(), curr_msg))
                        break
                    prev_msg = curr_msg
                if all_ok:
                    self.__commit_since_offset(prev_msg)

    def __commit_since_offset(self, msg: Message):
        topic_partition = TopicPartition(msg.get_topic(), msg.get_partition())
        self.__kafka_consumer.commit_async(
            {topic_partition: OffsetAndMetadata(msg.get_offset() + 1, topic_partition)}
        )

    def __read_batch(self):
        while True:
            batch = []
            for msg in self.__kafka_consumer:
                try:
                    offset, topic, partition = msg.offset, msg.topic, msg.partition
                    json_decoded = json.loads(msg.value.decode())
                    batch.append((offset, topic, partition, json_decoded))
                    if len(batch) >= self.__batch_size:
                        yield batch
                        batch = []
                        continue
                except JSONDecodeError as x:
                    logging.error('Received message cannot be json decoded.', msg)
            yield batch
