# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo
from scrapy.utils import project

settings = project.get_project_settings()
logger = logging.getLogger(__name__)

class BuaaMongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        self.db = self.client['edu_source']
        self.collection = self.db['buaa']

    def process_item(self, item, spider):
        try:
            self.collection.insert(dict(item))
        except Exception as e:
            logger.error(e)
        return item

    def close_spider(self, spider):
        self.client.close()


class LibBuaaMongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        self.db = self.client['edu_source']
        self.collection = self.db['lib_buaa']

    def process_item(self, item, spider):
        try:
            self.collection.insert(dict(item))
        except Exception as e:
            logger.error(e)
        return item

    def close_spider(self, spider):
        self.client.close()

class WanfangMongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        self.db = self.client['edu_source']
        self.collection = self.db['wanfang']

    def process_item(self, item, spider):
        try:
            self.collection.insert(dict(item))
        except Exception as e:
            logger.error(e)
        return item

    def close_spider(self, spider):
        self.client.close()

class BaidubaikeMongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        self.db = self.client['edu_source']
        self.collection = self.db['baidubaike']

    def process_item(self, item, spider):
        try:
            self.collection.insert(dict(item))
        except Exception as e:
            logger.error(e)
        return item

    def close_spider(self, spider):
        self.client.close()

class Open163MongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        self.db = self.client['edu_source']
        self.collection = self.db['open163']

    def process_item(self, item, spider):
        try:
            self.collection.insert(dict(item))
        except Exception as e:
            logger.error(e)
        return item

    def close_spider(self, spider):
        self.client.close()

class KeqqMongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        self.db = self.client['edu_source']
        self.collection = self.db['keqq']

    def process_item(self, item, spider):
        try:
            self.collection.insert(dict(item))
        except Exception as e:
            logger.error(e)
        return item

    def close_spider(self, spider):
        self.client.close()