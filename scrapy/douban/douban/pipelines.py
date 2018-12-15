# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings


class DoubanPipeline(object):

    def __init__(self):

        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        sheetname = settings['MONGODB_SHEETNAME']

        client = pymongo.MongoClient(host=host, port=port)

        mydb = client[dbname]

        self.sheet = mydb[sheetname]


    def process_item(self, item, spider):
        data = dict(item)
        self.sheet.insert(data)

        return item
