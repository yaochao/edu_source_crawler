#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/3/30
import copy

from scrapy import Spider, Request
from edu_source_crawler.misc.coursekeyword import keywords
from edu_source_crawler.items import WanfangItem

class WanfangSpider(Spider):
    name = 'wanfang'
    search_url = 'http://s.g.wanfangdata.com.cn/Paper.aspx?q='
    custom_settings = {
        'ITEM_PIPELINES': {
            'edu_source_crawler.pipelines.WanfangMongoPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'edu_source_crawler.misc.middlewares.UserAgentMiddleware': 400,
        },
        'DOWNLOAD_TIMEOUT': 10,
    }

    def start_requests(self):
        item = WanfangItem()
        for index, i in enumerate(keywords):
            for keyword in i:
                url = self.search_url + keyword
                request = Request(url=url, callback=self.parse1)
                item['course_type'] = index
                request.meta['item'] = copy.deepcopy(item)
                yield request

    def parse1(self, response):
        item = response.meta['item']
        uls = response.xpath('//*[@class="list_ul"]')
        for ul in uls:
            item['title'] = ul.xpath('li[1]/a[3]')[0].xpath('string(.)').extract_first()
            item['url'] = ul.xpath('li[1]/a[3]/@href').extract_first()
            item['subtitle'] = ul.xpath('li[2]')[0].xpath('string(.)').extract_first()
            item['_id'] = item['url']
            yield item

        # next url
        next_url = response.xpath(u'//t[text()="下一页"]/parent::a/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            request = Request(url=next_url, callback=self.parse1)
            request.meta['item'] = copy.deepcopy(response.meta['item'])
            yield request