import logging
import time
from typing import Final, Iterator, List, Optional

from confluent_kafka import Consumer, KafkaError, KafkaException
from confluent_kafka import Message as RawMessage

from dh_potluck.decorators import retry
from dh_potluck.messaging import Message, MessageEnvelopeSchema
from dh_potluck.messaging.exceptions import CommitTimeoutException
from dh_potluck.messaging.typings import ConsumerConfig
from dh_potluck.messaging.utils import build_consumer_config

RETRYABLE_COMMIT_ERROR_MAP: Final = {
    KafkaError.REQUEST_TIMED_OUT: CommitTimeoutException,
}

LOG = logging.getLogger(__name__)


class BatchingMessageConsumer:

    _consumer: Consumer
    _batch_size: int
    _release_after: float
    _auto_commit: bool
    _poll_timeout: float
    _shutdown: bool
    _batch_results: List[Message]
    _batch_deadline: Optional[float]
    _message_schema: MessageEnvelopeSchema = MessageEnvelopeSchema()

    def __init__(
        self,
        consumer_group_id: str,
        batch_size: int,
        release_after: float,
        auto_commit: bool = True,
        poll_timeout: float = 1.0,
        config_overrides: Optional[ConsumerConfig] = None,
        brokers: Optional[str] = None,
        should_connect_ssl: Optional[bool] = None,
    ) -> None:
        """
        BatchingMessageConsumer is a consumer that waits to collect batches of messages before
        releasing them for consumption
        :param str consumer_group_id: The kafka consumer group ID to use
        :param int batch_size: The max number of messages to collect before releasing a batch
        :param float release_after: How long to wait before releasing a batch if batch_size isn't
            exceeded (in milliseconds)
        :param bool auto_commit: If truthy, BatchingMessageConsumer will commit offsets for a batch
            under the hood. If falsy, then developers will be responsible for this behavior
        :param float poll_timeout: The poll_timeout config to pass to the inner Kafka consumer
        :param dict config_overrides: Custom config to pass to the inner Kafka consumer
        :param str brokers: list of brokers to connect to (also can be provided via the flask
            config `KAFKA_BROKERS_LIST`)
        :param bool should_connect_ssl: if a ssl connection should be used to kafka (also can be
            provided via the flask config `KAFKA_USE_SSL_CONNECTION`)
        """
        self._consumer = Consumer(
            build_consumer_config(consumer_group_id, config_overrides, brokers, should_connect_ssl)
        )
        self._batch_size = batch_size
        self._release_after = release_after
        self._auto_commit = auto_commit
        self._poll_timeout = poll_timeout
        self._shutdown = False
        self._batch_results = []
        self._batch_deadline = None

    def subscribe(self, topics: List[str]) -> None:
        """
        Subscribe to a list of topics
        :param list[str] topics: The list of topics to subscribe to
        """
        LOG.debug(f'Subscribing batching consumer to topics: {topics}')
        self._consumer.subscribe(topics)

    def get_batches(self) -> Iterator[List[Message]]:
        """
        Get messages from topic(s) and yield batches of them
        :return: Iterator[Message]
        """
        LOG.debug('Starting batching consumer')
        while not self._shutdown:
            if self._should_release_batch():
                LOG.debug('Releasing batch')
                yield self._batch_results
                if self._auto_commit:
                    self._do_auto_commit()
                self._do_reset_batch_state()
            self._do_poll_for_raw_messages()
        self._do_shutdown()

    def commit(self, messages: List[Message], asynchronous: bool = False) -> None:
        """
        Commit offsets for a list of Messages
        :param list[Message] messages: The list of messages to commit for
        :param bool asynchronous: Controls if commits should be async
        """
        LOG.debug(f'Manually committing offsets for {len(messages)} messages')
        for m in messages:
            self._consumer.commit(message=m, asynchronous=asynchronous)

    def force_shutdown(self) -> None:
        """
        Forcibly shutdown the batching consumer / polling loop
        """
        LOG.debug('Force shutting down batching consumer')
        self._shutdown = True

    def _do_poll_for_raw_messages(self) -> None:
        """
        Poll topic(s) for messages and pass them along for collection into batches
        """
        raw_message = self._consumer.poll(timeout=self._poll_timeout)
        if raw_message is None:
            return
        err = raw_message.error()
        if err:
            LOG.error(f'Consumer error: {err}')
            return
        self._do_collect_raw_message(raw_message)

    def _do_collect_raw_message(self, raw_message: RawMessage) -> None:
        """
        Collect a raw Kafka message, transform it into a DH message and collect it in a batch
        :param RawMessage raw_message: The raw Kafka message object
        """
        if not self._batch_deadline:
            self._batch_deadline = self._release_after / 1000.0 + time.time()

        message_value_str = raw_message.value().decode('utf-8')
        message_value = self._message_schema.loads(message_value_str)
        LOG.debug(f'Received message: {message_value_str}')
        self._batch_results.append(Message(raw_message.topic(), message_value, raw_message))

    def _should_release_batch(self) -> bool:
        """
        Checks to see if a batch should be released, truthy if batch size or deadline is exceeded
        :return bool:
        """
        batch_size_exceeded = len(self._batch_results) >= self._batch_size
        batch_deadline_exceeded = (
            self._batch_deadline is not None and time.time() > self._batch_deadline
        )
        return batch_size_exceeded or batch_deadline_exceeded

    @retry(RETRYABLE_COMMIT_ERROR_MAP.values())
    def _do_auto_commit(self) -> None:
        """
        Commit offsets for batch of messages synchronously. Does expo. retries on network timeouts
        """
        LOG.debug('Attempting to auto-commit for latest batch released')
        try:
            offsets = self._consumer.commit(asynchronous=False)
            LOG.debug(f'Committed offsets: {offsets}')
        except KafkaException as exc:
            raise RETRYABLE_COMMIT_ERROR_MAP.get(exc.args[0].code(), exc)

    def _do_reset_batch_state(self) -> None:
        """
        Reset the batch state back to the default
        """
        LOG.debug('Resetting batch state')
        self._batch_results = []
        self._batch_deadline = None

    def _do_shutdown(self) -> None:
        """
        Flush out the batch state and close the connection to the topic(s)
        """
        LOG.debug('Stopping batching consumer')
        self._do_reset_batch_state()
        self._consumer.close()
        LOG.debug('Stopped batching consumer')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._do_shutdown()

    @property
    def auto_commit(self) -> bool:
        return self._auto_commit
