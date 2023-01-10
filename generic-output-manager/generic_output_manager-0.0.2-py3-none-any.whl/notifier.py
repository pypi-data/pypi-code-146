from kafka import KafkaProducer
from bdaserviceutils import get_kafka_binder_brokers
import json

class Notifier:
    def __init__(self, topic) -> None:
        
        self.isActive = False

        if get_kafka_binder_brokers() is not None:
            self.producer = KafkaProducer(bootstrap_servers=[get_kafka_binder_brokers()])
            self.topic = topic
            self.isActive = True

    def something_has_changed(self, metadata):
        if self.isActive:
            message = {"message": "Generic output updated", "metatada": metadata.get()}
            self.producer.send(self.topic, json.dumps(message).encode('utf-8'))

