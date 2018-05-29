# -*- coding: utf-8 -*-
import hashlib

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from consumer.items import DownloaderItem


class DownloadSpider(RedisCrawlSpider):
    name = "downloader"

    custom_settings = {
        'ITEM_PIPELINES': {
            'consumer.pipelines.DownloaderPipeline': 400
        },
        'EXTENSIONS': {
            'consumer.patcher.NewspaperPatcher': None,
            'consumer.scheduler_index.MakeSaveRequest': None,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'consumer.middlewares.ConsumerDownloaderMiddleware': None,
        },
        'DEPTH_LIMIT': 3,
        'LOG_LEVEL': 'WARNING',
        'CONCURRENT_REQUESTS':50

    }
    allowed_domains = ['sina.com.cn', 'sohu.com', 'ifeng.com']
    denied_domains = ['ka.sina.com.cn']
    redis_key = "downloader:start_urls"
    index_key = "downloader:index_urls"
    rules = (
        Rule(LinkExtractor(allow_domains=allowed_domains, deny_domains=denied_domains), callback='parse_a',
             follow=True),)

    def parse_a(self, response):
        item = DownloaderItem()

        item['_id'] = hashlib.md5(response.url.encode('utf-8')).hexdigest()
        item['url'] = response.url
        item['meta'] = response.meta
        item['html'] = response.body
        item['category'] = response.meta['link_text']
        yield item
