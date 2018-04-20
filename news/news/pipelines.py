# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging


class MongoPipeline(object):
    db = client = collection = ''
    def __init__(self):
        self.client =pymongo.MongoClient(
            settings['MONGODB_HOST'],
            settings['MONGODB_PORT']
        )
        self.db = self.client[settings['MONGODB_DATABASE']]

    def process_item(self, item, spider):
        self.collection = self.db[item.source]
        news = dict(item)
        self.collection.insert_one(news)
        return item
