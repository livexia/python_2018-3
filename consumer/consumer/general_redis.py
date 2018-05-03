import redis


class GeneralRedis():
    pool = redis.ConnectionPool(host='192.168.0.101', port=6380, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

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