from general_redis import GeneralRedis
import pickle
from urllib.parse import urlparse


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


def send_request():
    g = GeneralRedis()
    s = g.read_set('consumer:index_urls')
    for i in s:
        r = make_request(i)
        g.save_sorted_set('consumer:requests', r, -10)
        print(g)
