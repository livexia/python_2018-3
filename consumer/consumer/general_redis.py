import redis


class GeneralRedis():

    # pool = redis.ConnectionPool(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], decode_responses=True)

    def __init__(self, host, port):
        pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

    def save_list(self, key, value):
        self.r.sadd(key, value)

    def read_list(self, key):
        return self.r.get(key)

    def save_set(self, key, value):
        self.r.sadd(key, value)

    def read_set(self, key):
        return self.r.smembers(key)

    def save_sorted_set(self, key, score, value):
        self.r.zadd(key, score, value)

    def read_sorted_set(self, key):
        return self.r.smembers(key)

    def set_sismember(self, key, value):
        return self.r.sismember(key, value)