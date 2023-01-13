from .logger import logger
import time
import pika
from .utils import (
    get_partition_queue_name,
    get_backup_queue_name,
    get_dead_letter_queue_name,
)
from threading import Lock


class RabbitStore:

    EXCHANGE_OPTIONS = {
        'type': 'direct',
        'durable': True,
        'auto_delete': False,
    }

    QUEUE_OPTIONS = {
        'quorum': True,
        'lazy': True,
        'durable': True,
        'auto_delete': False,
        'backup': False,
        'dead_letters': True,
    }

    def __init__(
        self,
        user=None,
        password=None,
        host=None,
        port=None,
        vhost=None,
        exchange=None,
        max_retry_seconds=None,
        max_retries=None,
        sleep_seconds_on_retry=None,
        auto_ack=True,
        prefetch=None,
        partitions=None,
        exchange_options=None,
        queue_options=None,
        logger_options=None,
    ):
        logger.reload(**logger_options)

        self._user = user or 'guest'
        self._password = password or 'guest'
        self._host = host or 'localhost'
        self._port = port or 5672
        self._vhost = vhost or '/'
        self._exchange = exchange
        self._max_retry_seconds = max_retry_seconds or 0

        self._sleep_seconds_on_retry = sleep_seconds_on_retry or 1

        self._max_retries = max_retries or (
            self._max_retry_seconds / self._sleep_seconds_on_retry
        )

        self._auto_ack = auto_ack
        self._prefetch = prefetch or 10
        self._partitions = partitions or 1

        self._exchange_options = self.__class__.EXCHANGE_OPTIONS.copy()
        if exchange_options:
            self._exchange_options = self._exchange_options | exchange_options

        self._queue_options = self.__class__.QUEUE_OPTIONS.copy()
        if queue_options:
            self._queue_options = self._queue_options | queue_options

        self._rabbit_url = (
            f'amqp://{self._user}:{self._password }@{self._host}:{self._port}'
        )

        self._declared_logical_queues = set()
        self._message_retries = {}
        self._lock = Lock()

        self._connect()

    def is_rabbitmq_alive(self):
        connection = self._get_connection()
        try:
            # Provide a connection object so it can be closed
            self._get_channel(connection=connection)
            return True
        except Exception:
            return False
        finally:
            try:
                connection.close()
            except Exception:
                pass

    def _get_connection(self):
        return pika.BlockingConnection(
            pika.ConnectionParameters(
                self._host,
                self._port,
                self._vhost,
                pika.PlainCredentials(
                    self._user,
                    self._password,
                ),
            )
        )

    def thread_safe(function):

        def _(*args, **kwargs):
            instance = args[0]
            with instance._lock:
                return function(*args, **kwargs)

        return _

    def reconnect(function):

        def _(*args, **kwargs):
            retries = 0

            while True:
                try:
                    return function(*args, **kwargs)

                except Exception as error:
                    instance = args[0]
                    retries += 1
                    if (not instance._max_retries
                            or retries >= instance._max_retries):
                        raise error

                    logger.warning(
                        'Reconnecting... '
                        f'({retries}/{instance._max_retries})',
                        error=error
                    )

                    try:
                        instance._channel = instance._get_channel()
                    except Exception:
                        pass
                    time.sleep(instance._sleep_seconds_on_retry)

        return _

    @reconnect
    @thread_safe
    def _declare_exchange(self):
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type=self._exchange_options['type'],
            durable=self._exchange_options['durable'],
            auto_delete=self._exchange_options['auto_delete'],
        )

    @reconnect
    def _connect(self):
        self._channel = self._get_channel()
        self._declare_exchange()

    def _get_channel(
        self,
        prefetch=None,
        connection=None,
    ):
        if prefetch is None:
            prefetch = self._prefetch

        # Pika's connection is not thread-safe, can't be reused.
        # Thus, neither the channels belonging to it.
        if connection is None:
            connection = self._get_connection()

        channel = connection.channel()
        channel.confirm_delivery()
        channel.basic_qos(prefetch_count=prefetch)

        return channel

    def _declare_queue(
        self,
        queue,
        options,
        partition=None,
        dead_letter=False,
        backup=False,
    ):
        arguments = {}
        if options['quorum']:
            arguments['x-queue-type'] = 'quorum'
        else:
            arguments['x-queue-type'] = 'classic'
            if options['lazy']:
                #  Quorum queues cannot be defined as lazy.
                arguments['x-queue-mode'] = 'lazy'

        dead_letter_queue = get_dead_letter_queue_name(queue)

        # Dead letter queueimage.png
        if dead_letter:
            queue_name = dead_letter_queue

        # Backup queue
        elif backup:
            backup_queue = get_backup_queue_name(queue, partition)
            queue_name = backup_queue

        # Partition queue
        else:
            self._declared_logical_queues.add(queue)
            partition_queue = get_partition_queue_name(queue, partition)
            queue_name = partition_queue

            if options['dead_letters']:
                arguments['x-dead-letter-exchange'] = self._exchange
                arguments['x-dead-letter-routing-key'] = dead_letter_queue

        self._channel.queue_declare(
            queue_name,
            durable=options['durable'],
            auto_delete=options['auto_delete'],
            arguments=arguments,
        )

        self._channel.queue_bind(
            exchange=self._exchange,
            queue=queue_name,
            routing_key=queue_name,
        )

    @reconnect
    @thread_safe
    def declare_queue(
        self,
        queue,
        options=None,
    ):
        if options is None:
            options = {}
        options = self._queue_options | options

        if options['dead_letters']:
            self._declare_queue(
                queue,
                options,
                dead_letter=True,
            )

        for partition in range(self._partitions):
            if options['backup']:
                self._declare_queue(
                    queue,
                    options,
                    partition=partition,
                    backup=True,
                )

            self._declare_queue(
                queue,
                options,
                partition=partition,
            )
