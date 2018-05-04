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
from newspaper import Article, Config, ArticleException


class ConsumerSpider(RedisCrawlSpider):
    name = "consumer"
    allowed_domains = ['sina.com.cn', 'sohu.com', 'ifeng.com']
    redis_key = "consumer:start_urls"
    index_key = "consumer:index_urls"
    # TODO: 增加更多的规则，限制index url的数量，以及排除部分关键字
    rules = (Rule(LinkExtractor(allow=(), allow_domains=allowed_domains), callback='parse_a', follow=True),)
    g = GeneralRedis()
    config = Config()
    config.fetch_images = False
    config.language = 'zh'

    def parse_a(self, response):
        item = BroadcrawlerItem()
        try:
            article = Article(url='', config=self.config)
            if response:
                article.download(input_html=response)
                article.parse()
                if article.is_news:
                    item['title'] = article.title
                    if isinstance(article.publish_date, datetime.datetime):
                        item['pubtime'] = article.publish_date.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        item['pubtime'] = "N/A"
                    item['content'] = article.text
                    item['url'] = response.url
                    item['author'] = article.authors
                    yield item
                else:
                    self.g.save_set('consumer:index_urls', response.url)

        except ArticleException:
            pass
