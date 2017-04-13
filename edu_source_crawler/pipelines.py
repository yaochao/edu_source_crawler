# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo
from scrapy.utils import project
import datetime, time

settings = project.get_project_settings()
logger = logging.getLogger(__name__)

class BuaaMongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        self.db = self.client['edu_source2']
        self.collection = self.db['buaa']
        self.index = 1

    def process_item(self, item, spider):
        item['index'] = self.index
        self.index += 1
        item['timestamp'] = int(time.mktime(datetime.datetime.now().timetuple()))
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
        self.db = self.client['edu_source2']
        self.collection = self.db['lib_buaa']
        self.index = 1

    def process_item(self, item, spider):
        item['index'] = self.index
        self.index += 1
        item['timestamp'] = int(time.mktime(datetime.datetime.now().timetuple()))
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
        self.db = self.client['edu_source2']
        self.collection = self.db['wanfang']
        self.index = 1

    def process_item(self, item, spider):
        item['index'] = self.index
        self.index += 1
        item['timestamp'] = int(time.mktime(datetime.datetime.now().timetuple()))
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
        self.db = self.client['edu_source2']
        self.collection = self.db['baidubaike']
        self.index = 1

    def process_item(self, item, spider):
        item['index'] = self.index
        self.index += 1
        item['timestamp'] = int(time.mktime(datetime.datetime.now().timetuple()))
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
        self.db = self.client['edu_source2']
        self.collection = self.db['open163']
        self.index = 1

    def process_item(self, item, spider):
        item['index'] = self.index
        self.index += 1
        item['timestamp'] = int(time.mktime(datetime.datetime.now().timetuple()))
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
        self.db = self.client['edu_source2']
        self.collection = self.db['keqq']
        self.index = 1

    def process_item(self, item, spider):
        item['index'] = self.index
        self.index += 1
        item['timestamp'] = int(time.mktime(datetime.datetime.now().timetuple()))
        try:
            self.collection.insert(dict(item))
        except Exception as e:
            logger.error(e)
        return item

    def close_spider(self, spider):
        self.client.close()

class TedMongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        self.db = self.client['edu_source2']
        self.collection = self.db['ted']
        self.index = 1

    def process_item(self, item, spider):
        item['index'] = self.index
        self.index += 1
        item['timestamp'] = int(time.mktime(datetime.datetime.now().timetuple()))
        try:
            self.collection.insert(dict(item))
        except Exception as e:
            logger.error(e)
        return item

    def close_spider(self, spider):
        self.client.close()

class It199MongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        self.db = self.client['edu_source2']
        self.collection = self.db['it199']
        self.index = 1

    def process_item(self, item, spider):
        item['index'] = self.index
        self.index += 1
        item['timestamp'] = int(time.mktime(datetime.datetime.now().timetuple()))
        try:
            self.collection.insert(dict(item))
        except Exception as e:
            logger.error(e)
        return item

    def close_spider(self, spider):
        self.client.close()