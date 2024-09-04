import paho.mqtt.client as mqtt
from typing import Callable, Any

class MQTTClient:
    def __init__(self, broker: str, port: int, topic: str):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.on_message_callback: Callable[[Any, Any, Any], None] | None = None

    def connect(self):
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(self.broker, self.port, 60)
        self.client.subscribe(self.topic)

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def _on_message(self, client, userdata, msg):
        if self.on_message_callback:
            self.on_message_callback(client, userdata, msg)
        else:
            print(f"Received message1: {msg.payload.decode()}")

    def set_on_message_callback(self, callback: Callable[[Any, Any, Any], None]):
        self.on_message_callback = callback

    def publish(self, message: str):
        self.client.publish(self.topic, message)

    def loop_forever(self):
        self.client.loop_forever()