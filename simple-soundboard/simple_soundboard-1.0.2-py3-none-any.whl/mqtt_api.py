import logging

from paho.mqtt import client as mqtt_client


class MQTTAPI:
    def __init__(self):
        self.mqtt = None
        self.subscribed_topic = ["simple_soundboard/#"]

    def start(self, mqtt_host, mqtt_port, mqtt_username, mqtt_password, callback):
        logging.info("Simple Soundboard starting")
        self.mqtt = mqtt_client.Client()
        self.mqtt.username_pw_set(mqtt_username, mqtt_password)
        self.mqtt.on_connect = self._on_connect
        self.mqtt.on_disconnect = self._on_disconnect
        self.mqtt.on_message = callback
        self.mqtt.connect_async(mqtt_host, mqtt_port)
        self.mqtt.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        logging.info("Simple Soundboard connected to MQTT")
        for topic in self.subscribed_topic:
            self.mqtt.subscribe(topic, qos=0)

    def _on_disconnect(self, client, userdata, rc):
        """MQTT Disconnect callback."""
        logging.error("Simple Soundboard lost MQTT connection")
