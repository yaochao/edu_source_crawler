#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/3/31

import scrapy

from edu_source_crawler.items import It199Item
from edu_source_crawler.misc.coursekeyword import keywords


class TedSpider(scrapy.Spider):
    name = 'it199'
    search_url = 'http://s.199it.com/cse/search?s=913566115233094367&entry=1&q='
    custom_settings = {
        'ITEM_PIPELINES': {
            'edu_source_crawler.pipelines.It199MongoPipeline': 300,
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
        divs = response.xpath('//div[@class="result f s0"]')
        for div in divs:
            item = It199Item()
            item['course_type'] = course_type
            item['url'] = response.urljoin(div.xpath('h3/a/@href').extract_first())
            item['_id'] = item['url']
            item['title'] = div.xpath('h3/a')[0].xpath('string(.)').extract_first()
            # TODO 👇不知道为什么img_url这个字段的xpath按照常理去写就不对，去掉a标签就可以获取到img_url
            item['img_url'] = div.xpath('div/div/table/tr/td/img/@src').extract_first()
            if item['img_url']:
                item['description'] = div.xpath('div/div[2]/div')[0].xpath('string(.)').extract_first()
            else:
                item['description'] = div.xpath('div/div/div')[0].xpath('string(.)').extract_first()
            yield item

        # next_page
        next_url = response.xpath(u'//a[text()="下一页>"]/@href').extract_first()
        print next_url
        if next_url:
            next_url = response.urljoin(next_url)
            print next_url
            request = scrapy.Request(url=next_url, callback=self.parse1)
            request.meta['course_type'] = course_type
            yield request
