#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import Session
from lxml import html
from urllib.parse import urlparse
import re


base_url = "http://sina.com.cn/"

# base_url = "http://sohu.com/"
def parse_index(base_url):
    session = Session()

    resp = session.get(base_url)
    resp.encoding = 'UTF-8'
    tree = html.fromstring(resp.text)

    links = set(tree.xpath("//@href"))
    netloc = urlparse(base_url).netloc

    valid_links = iter(set((urlparse(val).netloc for val in links if netloc in urlparse(val).netloc)))

    while 1:
        print("http://{}".format(next(valid_links)))
