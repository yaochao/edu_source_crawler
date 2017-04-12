#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/4/11

import scrapy

from edu_source_crawler.items import TedItem
from edu_source_crawler.misc.coursekeyword import keywords_en


class TedSpider(scrapy.Spider):
    name = 'ted'
    search_url = 'https://www.ted.com/search?q='
    custom_settings = {
        'ITEM_PIPELINES': {
            'edu_source_crawler.pipelines.TedMongoPipeline': 300,
        },
    }

    def start_requests(self):
        for index, i in enumerate(keywords_en):
            for keyword in i:
                request = scrapy.Request(url=self.search_url + keyword, callback=self.parse1)
                request.meta['course_type'] = index
                yield request

    def parse1(self, response):
        course_type = response.meta['course_type']
        articles = response.xpath('//article')
        for article in articles:
            item = TedItem()
            item['course_type'] = course_type
            item['url'] = response.urljoin(article.xpath('h3/a/@href').extract_first())
            item['_id'] = item['url']
            item['img_url'] = response.urljoin(article.xpath('div/div[1]/a/span/span/span/img/@src').extract_first())
            item['title'] = article.xpath('h3/a/text()').extract_first()
            item['description'] = article.xpath('div/div[2]/div[1]/text()').extract_first()
            yield item

        # next_page
        next_url = response.xpath('//a[text()="Next"]/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            request = scrapy.Request(url=next_url, callback=self.parse1)
            request.meta['course_type'] = course_type
            yield request
