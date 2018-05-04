# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo, logging

logger = logging.getLogger('MongoPipeline')


class ConsumerPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    logger = logging.getLogger('MongoPipeline')

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        # TODO: pipeline关于item的二次过滤，Mongo效率有待提高
        if len(item['title']) >= 15:
            data = dict(item)
            self.post.insert(data)
            return item
        else:
            logger.warn('DISCARD ITEM: ' + item['title'] + '\n' + item['url'])
