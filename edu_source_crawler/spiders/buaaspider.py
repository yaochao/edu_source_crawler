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
        total_page = response.xpath('//div[@class="page auto"]/text()').extract()[-1].strip().split('/')[-1]
        for i in range(1, int(total_page)):
            print 'page-%s' % i
            next_url = 'http://news.buaa.edu.cn/xswh/index' + str(i) + '.htm'
            yield Request(next_url)

    def parse_detail(self, response):
        item = response.meta['item']
        item['html_source'] = response.xpath('//*[@class="newsleftconbox auto"]').extract_first()
        item['html_text'] = response.xpath('//*[@class="newsleftconbox auto"]').xpath('string(.)').extract_first()
        item['type'] = self.map_type(item['html_text'])
        if item['type']:
            yield item

    def map_type(self, title):
        type1 = [u'学术活动', u'大家谈', u'学术报告', u'主题报告', u'院士茶座', u'讲座', u'大讲堂', u'学术论坛']
        type2 = [u'音乐厅', u'学生会', u'话剧']
        type3 = [u'创业', u'就业', u'招聘', u'实习', u'考研', u'公务员', u'专场']
        for i in type3:
            if i in title:
                return 3

        for i in type2:
            if i in title:
                return 2

        for i in type1:
            if i in title:
                return 1