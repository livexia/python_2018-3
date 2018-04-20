# encoding: utf-8

import scrapy

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["news.sohu.com",
                       "news.sina.com.cn",
                       "news.ifeng.com"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)