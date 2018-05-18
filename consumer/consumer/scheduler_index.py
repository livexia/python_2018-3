from .general_redis import GeneralRedis
from urllib.parse import urlparse
import pickle
import time
import logging
from scrapy import signals


class MakeSaveRequest():
    logger = logging.getLogger('Update request')
    timer = 0
    flag = 0

    def __init__(self, settings=None):
        self.s = settings
        self.start = time.clock()
        self.timer = time.clock()
        self.flag = 0

    @classmethod
    def from_crawler(cls, crawler):
        # instantiate the extension object
        ext = cls(crawler.settings)

        # connect the extension object to signals
        crawler.signals.connect(ext.send_request, signal=signals.engine_stopped)
        crawler.signals.connect(ext.send_request, signal=signals.engine_started)
        crawler.signals.connect(ext.send_request, signal=signals.item_scraped)
        # return the extension object
        return ext

    @staticmethod
    def make_request(url):
        p = urlparse(url)
        r = (p.scheme + "://" + p.netloc).encode('utf-8')
        d = {
            '_encoding': 'utf-8',
            'body': b'',
            'callback': '_response_downloaded',
            'cookies': {},
            'dont_filter': False,
            'errback': None,
            'flags': [],
            'headers': {b'Referer': [r]},
            'meta': {'depth': 1, 'link_text': '', 'rule': 0},
            'method': 'GET',
            'priority': 0,
            'url': url
        }
        return pickle.dumps(d)

    def insert_domain_request(self):
        g = GeneralRedis(self.s.get('REDIS_HOST'), self.s.get('REDIS_PORT'))
        s = g.read_set(self.s.get('WHITELIST_DOMAIN'))
        try:
            for i in s:
                r = self.make_request(i)
                g.save_sorted_set(self.s.get('REQUEST_KEY'), r, -10)
            self.logger.warning("Save {} requests successful".format(len(s)))
        except:
            self.logger.warning("Save {} requests failed".format(len(s)))

    def insert_url_request(self):
        g = GeneralRedis(self.s.get('REDIS_HOST'), self.s.get('REDIS_PORT'))
        s = g.read_set(self.s.get('WHITELIST_URL'))
        try:
            for i in s:
                r = self.make_request(i)
                g.save_sorted_set(self.s.get('REQUEST_KEY'), r, -5)
            self.logger.warning("Save {} requests successful".format(len(s)))
        except:
            self.logger.warning("Save {} requests failed".format(len(s)))

    def send_request(self):
        self.timer = time.clock() - self.start
        if 3600 < self.timer < 3600 + 1800 and self.flag == 0:
            self.insert_domain_request()
            self.flag = 1
            self.start = time.clock()
            self.logger.info("Send index to request")
        elif 3600 < self.timer < 3600 + 1800 and self.flag == 1:
            self.insert_domain_request()
            self.insert_url_request()
            self.flag = 0
            self.start = time.clock()
            self.logger.info("Send index to request")
