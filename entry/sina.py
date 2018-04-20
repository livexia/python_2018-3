#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  README.md
#  
#  Copyright 2018 夏国超 <livexia@MD101-Wire.lan>
#  
#
import requests
import re
import datetime
from itertools import count
from entry import general
import sys


def get_all():
    pass


def get_url(url, params):
    url_pattern = re.compile(r'(http.*?ml)')
    session = requests.Session()
    resp = session.get(url, params=params)
    url_list = url_pattern.findall(resp.text)
    return url_list
    # yield url_list


def get_old_url(date):
    url = 'http://news.sina.com.cn/old1000/news1000_{}.shtml'.format(date.strftime('%Y%m%d'))

    session = requests.Session()

    pass

def get_new_url(date):
    a = count(1)
    over = 1
    url = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php'
    params = {
        'col': '89',
        'date': date.strftime('%Y-%m-%d'),
        'num': '100',
        'page': 0
    }
    while over:
        params['page'] = next(a)

        url_pattern = re.compile(r'(http.*?ml)')
        session = requests.Session()
        resp = session.get(url, params=params)
        url_list = url_pattern.findall(resp.text)

        if url_list:
            url_iter = iter(url_list)
            try:
                while 1:
                    general.insert_into_mongodb('sina_news', {'_id': next(url_iter)})
            except Exception as e:
                print(e)
        else:
            print("{} is done".format(date))
            over = 0

def new_or_old(date):
    start_date = datetime.datetime(1999, 5, 26)
    new_date = datetime.datetime(2010, 3, 30)
    if date < start_date:
        return None
    if start_date <= date < new_date :
        return 'old'
    return 'new'

if __name__ == '__main__':

    date = datetime.datetime.now()
    if new_or_old(date) == 'new':
        get_new_url(date)
    elif new_or_old(date) == 'old':
        get_old_url(date)
    else:
        print("进入了过早的时间")
    sys.exit()
