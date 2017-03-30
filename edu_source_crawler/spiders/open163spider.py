#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/3/30
import re
import urllib

import scrapy

from edu_source_crawler.items import Open163Item
from edu_source_crawler.misc.coursekeyword import keywords


class Open163Spider(scrapy.Spider):
    name = 'open163'
    search_url = 'https://c.open.163.com/dwr/call/plaincall/OpenSearchBean.searchCourse.dwr'
    custom_settings = {
        'ITEM_PIPELINES': {
            'edu_source_crawler.pipelines.Open163MongoPipeline': 300,
        },
    }

    def start_requests(self):
        for index, i in enumerate(keywords):
            for keyword in i:
                body = """
    callCount=1
    scriptSessionId=${scriptSessionId}190
    httpSessionId=
    c0-scriptName=OpenSearchBean
    c0-methodName=searchCourse
    c0-id=0
    c0-param0=string: %s
    c0-param1=number:1
    c0-param2=number:2000
    batchId=1490864754815
                """ % urllib.quote(keyword)
                request = scrapy.Request(url=self.search_url, callback=self.parse1, method='POST', body=body)
                request.meta['course_type'] = index
                yield request

    def parse1(self, response):
        course_type = response.meta['course_type']
        body = response.body
        totleCount = int(re.findall(r'totleCount=(.*?);', body)[0])
        if totleCount == 0:
            return
        for i in range(2, totleCount + 2):
            item2 = Open163Item()
            item2['course_type'] = course_type
            img_url = re.findall(r's%s.bigPicUrl="(.*?)"' % i, body)[0]
            course_url = re.findall(r's%s.courseUrl="(.*?)"' % i, body)[0]
            description = re.findall(r's%s.description="(.*?)"' % i, body)[0].replace('{##', '').replace('##}', '')
            title = re.findall(r's%s.title="(.*?)"' % i, body)[0].replace('{##', '').replace('##}', '')
            item2['url'] = course_url
            item2['_id'] = course_url
            item2['img_url'] = img_url
            item2['description'] = eval("u'" + description + "'")
            item2['title'] = eval("u'" + title + "'")
            yield item2
