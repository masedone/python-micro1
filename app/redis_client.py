import redis
import os
import json

class RedisClient:
    def __init__(self):
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.db = int(os.getenv('REDIS_DB', 0))
        self.password = os.getenv('REDIS_PASSWORD', None)

        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True
        )

    def set_value(self, key: str, value: dict):
        self.client.set(key, json.dumps(value))

    def get_value(self, key: str):
        value = self.client.get(key)
        if value:
            return json.loads(value)
        return None 