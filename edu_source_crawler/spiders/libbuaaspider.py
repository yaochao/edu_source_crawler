#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/3/29
import copy

import scrapy
from scrapy import Request

from edu_source_crawler.items import LibBuaaItem
from edu_source_crawler.misc.coursekeyword import keywords


class LibBuaaspiderSpider(scrapy.Spider):
    name = "libbuaa"
    search_url = 'http://opac.lib.buaa.edu.cn/opac/openlink.php?title='
    custom_settings = {
        'ITEM_PIPELINES': {
            'edu_source_crawler.pipelines.LibBuaaMongoPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'edu_source_crawler.misc.middlewares.UserAgentMiddleware': 400,
        },
        'DOWNLOAD_TIMEOUT': 10,
    }

    def start_requests(self):
        item = LibBuaaItem()
        for index, i in enumerate(keywords):
            for keyword in i:
                url = self.search_url + keyword
                request = Request(url=url, callback=self.parse1)
                item['course_type'] = index
                request.meta['item'] = copy.deepcopy(item)
                yield request

    def parse1(self, response):
        item = response.meta['item']
        lis = response.xpath('//*[@id="search_book_list"]/li')
        for li in lis:
            title = li.xpath('h3/a/text()').extract_first()
            num = title.split(u'.')[0] + u'.'
            item['title'] = title.split(num)[-1]
            item['url'] = response.urljoin(li.xpath('h3/a/@href').extract_first())
            item['_id'] = item['url']
            request = Request(item['url'], self.parse_detail)
            request.meta['item'] = copy.deepcopy(item)
            yield request
        # next page
        next_url = response.urljoin(response.xpath('//*[@class="num_prev"]/a/@href').extract_first())
        if next_url:
            request = Request(url=next_url, callback=self.parse1)
            request.meta['item'] = copy.deepcopy(response.meta['item'])
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        author = response.xpath(u'//dt[text()="题名/责任者:"]/following::*[1]/text()').extract_first()
        item['author'] = author.split('/')[-1]
        publish_info = response.xpath(u'//dt[text()="出版发行项:"]/following::*[1]/text()').extract_first()
        publish_info = publish_info.split(':')[-1].split(',')
        item['publish_house'] = publish_info[0]
        item['publish_year'] = publish_info[-1]
        isbn = response.xpath(u'//dt[text()="ISBN及定价:"]/following::*[1]/text()').extract_first()
        item['isbn'] = isbn.split('/')[0]
        tds = response.xpath('//tr[@class="whitetext"]/td')
        for index, td in enumerate(tds):
            if index == 0:
                item['sushuhao'] = td.xpath('text()').extract_first()
            if index == 3:
                item['guancang'] = td.xpath('text()').extract_first()
            if index == 4:
                item['book_status'] = td.xpath('text()').extract_first()
        yield item
