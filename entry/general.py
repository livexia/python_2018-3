# encoding: utf-8

from pymongo import MongoClient
import sys


def insert_into_mongodb(col, date):
    try:
        client = MongoClient('localhost', 32679)
        db = client[col]
        posts = db.posts
        post_id = posts.insert_one(date).inserted_id
        print(post_id)
    except Exception as e:
        print(e)
        exit()