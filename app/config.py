import os

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq-release')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'test')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0)) 