#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/3/30

import scrapy

from edu_source_crawler.items import KeqqItem
from edu_source_crawler.misc.coursekeyword import keywords


class KeqqSpider(scrapy.Spider):
    name = 'keqq'
    search_url = 'https://ke.qq.com/course/list/'
    custom_settings = {
        'ITEM_PIPELINES': {
            'edu_source_crawler.pipelines.KeqqMongoPipeline': 300,
        },
    }

    def start_requests(self):
        for index, i in enumerate(keywords):
            for keyword in i:
                request = scrapy.Request(url=self.search_url + keyword, callback=self.parse1)
                request.meta['course_type'] = index
                yield request

    def parse1(self, response):
        course_type = response.meta['course_type']
        lis = response.xpath('//div[@class="market-bd market-bd-6 course-list course-card-list-multi-wrap"]/ul/li')
        for li in lis:
            item = KeqqItem()
            item['course_type'] = course_type
            item['url'] = li.xpath('a/@href').extract_first().strip()
            item['_id'] = item['url']
            item['img_url'] = 'https:' + li.xpath('a/img/@src').extract_first().strip()
            item['title'] = li.xpath('a/img/@alt').extract_first()
            item['description'] = li.xpath('div/span/text()').extract_first()
            yield item

        # next_page
        next_url = response.xpath('//*[@class="page-next-btn icon-font i-v-right "]/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            request = scrapy.Request(url=next_url, callback=self.parse1)
            request.meta['course_type'] = course_type
            yield request
