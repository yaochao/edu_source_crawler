#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/8/11

import random
from edu_source_crawler.misc.useragents import USER_AGENTS


# DownloadMiddleware
class UserAgentMiddleware(object):
    # 每当有request时,会自动调用此方法
    def process_request(self, request, spider):
        # user_agent = random.choice(USER_AGENTS) 因为里面有移动版的useragent,导致请求的页面是移动版本,从而使xpath出错或者找不到对应的内容。
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
        request.headers['User-Agent'] = user_agent
