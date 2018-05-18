# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo, logging
from scrapy.exceptions import DropItem
from consumer.general_redis import GeneralRedis
from urllib.parse import urlparse

logger = logging.getLogger('MongoPipeline')


class ConsumerPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, settings):
        self.s = settings
        host = self.s.get("MONGODB_HOST")
        port = self.s.get("MONGODB_PORT")
        dbname = self.s.get("MONGODB_DBNAME")
        sheetname = self.s.get("MONGODB_SHEETNAME")
        self.g = GeneralRedis(self.s.get('REDIS_HOST'), self.s.get('REDIS_PORT'))

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

                self.g.save_set(self.s.get('WHITELIST_DOMAINS'), data['url'])
                logging.info('Add domain on whitelist {}'.format(data['url']))

                # flag = input("{} type:".format(data['url']))
                # result = urlparse(data['url'])
                # domain_url = (result.scheme + "://" + result.netloc).encode('utf-8')
                # none_query_url = (result.scheme + "://" + result.netloc + result.path).encode('utf-8')
                #
                # if flag == '0':
                #     self.g.save_set(self.s.get('WHITELIST_DOMAINS'), domain_url)
                #     logging.info('Add domain on whitelist {}'.format(domain_url))
                # elif flag == '1':
                #     self.g.save_set(self.s.get('WHITELIST_URLS'), none_query_url)
                #     logging.info('Add domain on whitelist {}'.format(none_query_url))
                #
                # elif flag == '2':
                #     self.g.save_set(self.s.get('BLACKLIST_DOMAINS'), domain_url)
                #     logging.info('Add domain on blacklist {}'.format(domain_url))
                # elif flag == '3':
                #     self.g.save_set(self.s.get('BLACKLIST_URLS'), none_query_url)
                #     logging.info('Add domain on blacklist {}'.format(none_query_url))
                # elif flag == '4':
                #     url = input("input url to add blacklist：")
                #     self.g.save_set(self.s.get('BLACKLIST_URLS'), url)
                #     logging.info('Add domain on blacklist {}'.format(url))
                # else:
                #     pass


                raise DropItem("Index item found: %s" % item)
            else:
                match_doc = self.post.find_one({"_id": data['_id']})
                # TODO: 过滤以及id判定
                if match_doc:
                    # logger.debug("document existed", data)
                    raise DropItem("Duplicate item found: %s" % item)
                    # raise
                    # self.post.replace_one(match_doc, data)
                else:
                    self.post.insert_one(data)
                    return item
        except DropItem as e:
            pass
