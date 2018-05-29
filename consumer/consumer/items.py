# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndexItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()    #url
    pass


class BroadcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    pubtime = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    _id = scrapy.Field()


class DownloaderItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    html = scrapy.Field()
    category = scrapy.Field()
    meta = scrapy.Field()