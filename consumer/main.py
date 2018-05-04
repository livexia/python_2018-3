# -*- coding: utf-8 -*-
import sys, time
from scrapy import cmdline
import redis
from scheduler_index import MakeSaveRequest

if __name__ == '__main__':
    try:
        spider_name = sys.argv[1]
        print("Spider name:{}".format(spider_name))
    except Exception:
        spider_name = input("Spider name:")
    # s = MakeSaveRequest()
    # s.send_request()
    # exit(0)
    cmdline.execute("scrapy crawl {}".format(spider_name).split())

