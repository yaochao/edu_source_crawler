#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/3/30
import copy

import scrapy
from edu_source_crawler.misc.coursekeyword import baikekeywords
from edu_source_crawler.items import BaidubaikeItem

class BaidubaikeSpider(scrapy.Spider):
    name = 'baidubaike'
    search_url = 'http://baike.baidu.com/item/'
    custom_settings = {
        'ITEM_PIPELINES': {
            'edu_source_crawler.pipelines.BaidubaikeMongoPipeline': 300,
        },
    }

    def start_requests(self):
        item = BaidubaikeItem()
        for keyword in baikekeywords:
            url = self.search_url + keyword
            request = scrapy.Request(url=url, callback=self.parse1)
            item['keyword'] = keyword
            request.meta['item'] = copy.deepcopy(item)
            yield request

    def parse1(self, response):
        item = response.meta['item']
        item['_id'] = response.url
        item['url'] = response.url
        item['header_text'] = response.xpath('//div[@label-module="lemmaSummary"]')[0].xpath('string(.)').extract_first()
        paras = response.xpath('//div[@class="main-content"]/div[@label-module="para"]')
        body_text = ''
        for para in paras:
            body_text += para.xpath('string(.)').extract_first()
        item['body_text'] = body_text.replace('\n', '')
        item['html_source'] = response.xpath('//div[@class="main-content"]').extract_first()
        yield item