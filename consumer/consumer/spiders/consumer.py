# -*- coding: utf-8 -*-
import hashlib

from scrapy.spiders import Rule
# from scrapy.settings import Settings
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider
from consumer.items import IndexItem, BroadcrawlerItem
import datetime

from newspaper import Article, Config, ArticleException

deny_regex = 'slide|blog|auto|weibo|baby|vip|book|picture|photo|video|tags|comment|models|ishare|iask'

class ConsumerSpider(RedisCrawlSpider):
    name = "consumer"
    allowed_domains = ['sina.com.cn', 'sohu.com', 'ifeng.com']
    # allowed_domains = ['news.sina.com.cn']
    denied_domains = ['ka.sina.com.cn']
    redis_key = "consumer:start_urls"
    index_key = "consumer:index_urls"
    # TODO: 增加更多的规则，限制index url的数量，以及排除部分关键字
    rules = (Rule(LinkExtractor(deny=deny_regex, allow_domains=allowed_domains, deny_domains=denied_domains), callback='parse_a', follow=True),)
    # s = Crq.settings
    # g = GeneralRedis(settings.get('REDIS_HOST'), settings.get('REDIS_PORT'))
    # print(s.get('REDIS_HOST'), s.get('REDIS_PORT'))
    # exit()
    config = Config()
    config.fetch_images = False
    config.language = 'zh'

    # TODO: meta 中舍弃2016年前的，添加标题正文相识度匹配过滤垃圾内容
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
                    item['_id'] = hashlib.md5(response.url.encode('utf-8')).hexdigest()
                    yield item
                else:
                    item = IndexItem()
                    item['url'] = response.url
                    yield item
                    # self.g.save_set('consumer:index_urls', response.url)

        except ArticleException:
            pass
