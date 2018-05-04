from general_redis import GeneralRedis
from urllib.parse import urlparse
import pickle
import logging
from scrapy import signals


class MakeSaveRequest():
    logger = logging.getLogger('Update request')

    @classmethod
    def from_crawler(cls, crawler):
        # instantiate the extension object
        ext = cls()

        # connect the extension object to signals
        crawler.signals.connect(ext.send_request, signal=signals.engine_stopped)

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

    def send_request(self):
        g = GeneralRedis()
        s = g.read_set('consumer:index_urls')
        try:
            for i in s:
                r = self.make_request(i)
                g.save_sorted_set('consumer:requests', r, -10)
            self.logger.warning("Save {} requests successful".format(len(s)))
        except:
            self.logger.warning("Save {} requests failed".format(len(s)))
