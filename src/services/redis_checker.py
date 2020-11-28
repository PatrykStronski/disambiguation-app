import redis

class RedisChecker:
    host = "redis"
    db = 0
    redis_instance = None
    def __init__(self):
        self.redis_instance = redis.Redis(host=self.host, db=self.db)

    def insert_processed_id(self, uri):
        self.redis_instance.set(hash(uri), "DONE")

    def get_processed_id(self, uri):
        return self.redis_instance.get(hash(uri))
