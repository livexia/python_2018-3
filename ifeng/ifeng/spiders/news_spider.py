# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from ifeng.items import NewsItem
import itertools
import datetime
import re


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["ifeng.com"]
    #{0}:新闻类型，{1}:时间，{2}:页数
    #类型：{'11528': '大陆', '11574': '国际', '11502': '即时'}
    news_base_url = 'http://news.ifeng.com/listpage/{0}/{1}/{2}/rtlist.shtml'
    today = datetime.datetime.now().strftime("%Y%m%d")
    start_urls = [news_base_url.format('11528',20180317,1)]
    print(start_urls)


    def parse(self, response):
        resp = Selector(response)
        url = iter(resp.xpath('.//div[@class="newsList"]//li/a/@href').extract())

        try:
            while 1:
                news_url = next(url)
                yield Request(news_url, meta= {'key': re.search('a\/(.*?)\.', news_url).group(1), 'url' : news_url}, callback=self.parse_news)
        except StopIteration:
            url = resp.xpath('.//div[@class="m_page"]//a/@href').extract()
            if url:
                print("爬取下一页")
                yield Request(url[0], callback=self.parse)

    def parse_news(self, response):
        #获得新闻内容
        news = NewsItem()

        resp = Selector(response)
        news['url'] = response.meta['url']
        news['_id'] = response.meta['key']

        try:
            news['title'] = resp.xpath('.//h1//text()').extract()[0]
            news['date'] = resp.xpath('.//span[@itemprop="datePublished"]//text()').extract()[0]
            news['source'] = resp.xpath('.//span[@itemprop="publisher"]//text()').extract()[0]
            news['content'] = resp.xpath('.//div[@id="main_content"]//text()').extract()
        except IndexError:
            news['title'] = resp.xpath('.//h1//text()').extract()[0]
            news['date'] = resp.xpath('.//div[@class="yc_tit"]//p//span//text()').extract()[0]
            news['source'] = resp.xpath('.//div[@class="yc_tit"]//p//a//text()').extract()[0]
            news['content'] = resp.xpath('.//div[@id="yc_con_txt"]//text()').extract()
        yield news