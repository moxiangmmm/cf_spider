# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import base64
import redis
from scrapy import exceptions
import re
import hashlib

class CfSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RrandomUA:
    def process_request(self,request,spider):
        now_ua = random.choice(spider.settings.get("USER_AGENTS"))
        # print('+'*20,now_ua)
        request.headers["User-Agent"] = now_ua



proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H65403216IJKN42D"
proxyPass = "55697F9CCB86225E"

# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
# 阿布云代理
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth


class Gl_url(object):
    def process_request(self, request, spider):
        if spider.name == 'bj_pro':
            # print("+"*20,request)
            # print(request.body)
            # print(request.method)
            if request.method == "GET":
                # # http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/001607220057212582?_=1518077185819
                ret_url = re.sub(r'_=(.*?)&', '', request.url)
                request_exit = self.request_dupfilter(ret_url, spider)
                if not request_exit:
                    # 如果是新的请求
                    print("=" * 50)
                    return None
                else:
                    print("0"*50)
                    raise exceptions.IgnoreRequest
            elif request.method == "POST":
                # ret_body = re.sub(r'&=(.*?)&', '', request.body.decode())
                ret = request.url + request.body.decode()
                request_exit = self.request_dupfilter(ret, spider)
                if not request_exit:
                    # 如果是新的请求
                    print("=" * 50)
                    return None
                else:
                    print("0"*20)
                    raise exceptions.IgnoreRequest

    # 数据去重
    def request_dupfilter(self, p_str, spider):
        if spider.name == 'bj_pro':
            self.r = redis.Redis(host='127.0.0.1', port=6379, db=5)
            self.item_key = "cf_request_dumpkey"
            f = hashlib.sha1()
            f.update(p_str.encode())
            fingerprint = f.hexdigest()
            added = self.r.sadd(self.item_key, fingerprint)
            return added == 0
