# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BuaaItem(Item):
    _id = Field()
    title = Field()
    url = Field()
    html_source = Field()
    html_text = Field()
    type = Field()


class LibBuaaItem(Item):
    _id = Field()
    title = Field()
    url = Field()
    course_type = Field()
    author = Field()
    publish_house = Field()
    publish_year = Field()
    isbn = Field()
    sushuhao = Field()
    guancang = Field()
    book_status = Field()

class WanfangItem(Item):
    _id = Field()
    title = Field()
    subtitle = Field()
    url = Field()
    course_type = Field()
