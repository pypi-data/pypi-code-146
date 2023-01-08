import time

import pika


class RobustConnection():
    def __init__(self, connection_parameters_kwargs, exchange_kwargs):
        self._connection_parameters_kwargs = connection_parameters_kwargs
        self._exchange_kwargs = exchange_kwargs
        self._connection = None
        self._channel = None
        self.connect()
        
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        self.disconnect()
    
    def _setup_connection(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(**self._connection_parameters_kwargs))
        
    def _setup_channel(self):
        self._channel = self._connection.channel()
    
    def _setup_exchange(self):
        self._channel.exchange_declare(**self._exchange_kwargs)
    
    def _connect(self):
        self._setup_connection()
        self._setup_channel()
        self._setup_exchange()
    
    def connect(self):
        if (self._connection is None) or self._connection.is_closed:
            while True:
                try:
                    self._connect()
                    break
                except (pika.exceptions.ConnectionClosedByBroker, pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError, pika.exceptions.IncompatibleProtocolError):
                    time.sleep(1.0)
                    continue
        
    def disconnect(self):
        if self._connection is not None:
            self._connection.close()
        
    def retry(self, f, *args, **kwargs):
        while True:
            try:
                self._setup_exchange()
                f(*args, **kwargs)
                break
            except (pika.exceptions.ConnectionClosedByBroker, pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError, pika.exceptions.IncompatibleProtocolError) as e:
                time.sleep(1.0)
                self.connect()
                continue
        

class Publisher(RobustConnection):
    def _publish(self, routing_key, body):
        self._channel.basic_publish(
            exchange=self._exchange_kwargs["exchange"],
            routing_key=routing_key,
            body=body,
        )
        
    def publish(self, *args, **kwargs):
        self.retry(f=self._publish, *args, **kwargs)


class Consumer(RobustConnection):
    def __init__(self, connection_parameters_kwargs, exchange_kwargs, queue_kwargs, bind_kwargs, consume_kwargss, prefetch_count=None):
        self._queue_kwargs = queue_kwargs
        self._bind_kwargs = bind_kwargs
        self._consume_kwargss = consume_kwargss
        self._prefetch_count = prefetch_count
        self._queue_name = None
        super().__init__(connection_parameters_kwargs=connection_parameters_kwargs, exchange_kwargs=exchange_kwargs)

    def _setup_channel(self):
        super()._setup_channel()
        if self._prefetch_count is not None:
            self._channel.basic_qos(prefetch_count=self._prefetch_count)

    def _setup_queue(self):
        result = self._channel.queue_declare(**self._queue_kwargs)
        self._queue_name = result.method.queue
        self._channel.queue_bind(**self._bind_kwargs, queue=self._queue_name, exchange=self._exchange_kwargs["exchange"], )

    def _setup_consume(self):
        for consume_kwargs in self._consume_kwargss:
            if ("queue" in consume_kwargs) and (consume_kwargs["queue"] is None):
                consume_kwargs = self._queue_name
            self._channel.basic_consume(**consume_kwargs)

    def _connect(self):
        super()._connect()
        self._setup_queue()
        self._setup_consume()
    
    def _start_consuming(self):
        self._channel.start_consuming()
        
    def start_consuming(self):
        self.retry(f=self._start_consuming)

