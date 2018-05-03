# -*- coding: utf-8 -*-
import sys, time
from scrapy import cmdline
from scrapy.http import Request
import redis
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider, RedisMixin
from scheduler_index import send_request

class GeneralRedis():
    pool = redis.ConnectionPool(host='192.168.0.101', port=6380, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    def save_to_redis(self, key, value):
        self.r.sadd(key, value)

    def read_from_redis(self, key):
        return self.r.get(key)


if __name__ == '__main__':
    try:
        spider_name = sys.argv[1]
        print("Spider name:{}".format(spider_name))
    except Exception:
        spider_name = input("Spider name:")
    cmdline.execute("scrapy crawl {}".format(spider_name).split())
    print(12332143231432423543253453453)
    while True:
        send_request()
        time.sleep(3600)
