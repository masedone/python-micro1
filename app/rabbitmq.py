import pika
import os
import json

class RabbitMQClient:
    def __init__(self):
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))
        self.queue = os.getenv('RABBITMQ_QUEUE', 'test')
        self.user = os.getenv('RABBITMQ_USER', 'admin')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'admin123')

        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

    def send_message(self, message: dict):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def close(self):
        self.connection.close() 