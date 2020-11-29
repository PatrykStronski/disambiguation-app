import redis

class RedisChecker:
    host = "redis"
    db = 0
    redis_instance = None
    def __init__(self):
        self.redis_instance = redis.Redis(host=self.host, db=self.db)

    def insert_processed_id(self, uri):
        print(self.redis_instance.set(uri, "DONE"))

    def get_processed_id(self, uri):
        result = self.redis_instance.get(uri)
        if result:
            return result.decode('utf-8')
