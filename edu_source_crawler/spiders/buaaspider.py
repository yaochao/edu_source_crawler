#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/3/29
import copy

import scrapy
from scrapy import Request

from edu_source_crawler.items import BuaaItem


class BuaaspiderSpider(scrapy.Spider):
    name = "buaa"
    start_urls = ['http://news.buaa.edu.cn/xswh/index.htm']
    custom_settings = {
        'ITEM_PIPELINES': {
            'edu_source_crawler.pipelines.BuaaMongoPipeline': 300,
        },
    }

    def parse(self, response):
        item = BuaaItem()
        divs = response.xpath('//*[@class="listlefttop auto"]/div')
        for div in divs:
            item['title'] = div.xpath('h2/a/text()').extract_first()
            item['url'] = response.urljoin(div.xpath('h2/a/@href').extract_first())
            item['_id'] = item['url']
            request = Request(item['url'], self.parse_detail)
            request.meta['item'] = copy.deepcopy(item)
            yield request

        # next page
        for i in range(1, 80):
            next_url = 'http://news.buaa.edu.cn/xswh/index' + str(i) + '.htm'
            yield Request(next_url)

    def parse_detail(self, response):
        item = response.meta['item']
        item['html_source'] = response.xpath('//*[@class="newsleftconbox auto"]').extract_first()
        item['html_text'] = response.xpath('//*[@class="newsleftconbox auto"]').xpath('string(.)').extract_first()
        item['type'] = self.map_type(item['title'])
        if item['type']:
            yield item

    def map_type(self, title):
        type1 = [u'飞行', u'空中领航', u'飞机']
        type2 = [u'大赛', u'讲座', u'学生会', u'社团']
        type3 = [u'实习', u'就业', u'招聘']
        for i in type1:
            if i in title:
                return 1

        for i in type2:
            if i in title:
                return 2

        for i in type3:
            if i in title:
                return 3
