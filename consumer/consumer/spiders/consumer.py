# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider
from consumer.items import ConsumerItem, BroadcrawlerItem
from consumer.general_redis import GeneralRedis
import itertools
import datetime
import re
from newspaper import Article, Config


class ConsumerSpider(RedisCrawlSpider):
    name = "consumer"
    allowed_domains = ['sina.com.cn', 'sohu.com', 'ifeng.com']
    redis_key = "consumer:start_urls"
    index_key = "consumer:index_urls"
    rules = (Rule(LinkExtractor(allow=()), callback='parse_a', follow=True),)
    g = GeneralRedis()
    c = Config()
    c.fetch_images = False
    def parse_a(self, response):
        news= BroadcrawlerItem()
        a = Article('', language='zh', config=self.c)
        resp = response.body
        a.download(input_html=resp)
        a.parse()

        urls = LinkExtractor(allow=(), allow_domains=self.allowed_domains).extract_links(response)

        if len(urls) > 30:
            self.g.save_list(self.index_key, response.url)

        print(response.url)
        news['title'] = a.title
        news['pubtime'] = a.publish_date
        news['url'] = response.url
        news['content'] = a.text
        news['author'] = a.authors
        yield news
