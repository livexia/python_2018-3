# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo, logging
from scrapy.exceptions import DropItem
from consumer.general_redis import GeneralRedis



logger = logging.getLogger('MongoPipeline')


class ConsumerPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, settings):
        host = settings.get("MONGODB_HOST")
        port = settings.get("MONGODB_PORT")
        dbname = settings.get("MONGODB_DBNAME")
        sheetname = settings.get("MONGODB_SHEETNAME")
        self.g = GeneralRedis(settings.get('REDIS_HOST'), settings.get('REDIS_PORT'))

        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        data = dict(item)
        try:
            if type(item).__name__ == 'IndexItem':
                self.g.save_set('consumer:index_urls', data['url'])
                raise DropItem("Index item found: %s" % item)
            else:
                match_doc = self.post.find_one({"_id": data['_id']})
                #TODO: 过滤以及id判定
                if match_doc:
                    # logger.debug("document existed", data)
                    raise DropItem("Duplicate item found: %s" % item)
                    # raise
                    # self.post.replace_one(match_doc, data)
                else:
                    self.post.insert_one(data)
                return item
        except DropItem as e:
            print(e)