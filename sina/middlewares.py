# encoding: utf-8
import random
import yaml
from sina.cookies import cookies, init_cookies
from sina.user_agents import agents
from redis import StrictRedis
from time import sleep
import requests
import pymongo

import logging
from logging.handlers import RotatingFileHandler
from scrapy.downloadermiddlewares.retry import RetryMiddleware

logger = logging.getLogger(__name__)

class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """

    def __init__(self):
        init_cookies()

    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        request.cookies = cookie

class ResponseNotWorkMiddleware(object):
    
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["Sina"]
        self.proxies = self.db["proxies"]

    def process_response(self, request, response, spider):  
        return response

    def process_exception(self, request, exception, spider):
        logger = logging.getLogger(__name__)
        logger.warning('Not Work process_exception...')
        logger.warning(exception)

        if ('User timeout caused' in str(exception)):
            sleep(20)
            return request

        self.get()
        sleep(20)
        proxy = self.get_random_proxy()  
        print("Not Work this is request ip:"+proxy)  
        request.meta['proxy'] = proxy
        request.dont_filter=True
        logger.warning('Not Work over!')
        return request
    
    def get(self):
        while(True):
            try:
                r = requests.get("http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD20187195466ArkBQ1/c711f5747db611e7bcaf7cd30abda612?returnType=2",
                        timeout=120)
            except Exception as err_info:
                r = None
                print(err_info)

            if r is not None:
                print(r.status_code)
                if r.status_code == 200:
                    print(r.content)
                    print(r.json())
                    result = r.json()
                    if result["ERRORCODE"] == "0" and result["RESULT"]:
                        one = result["RESULT"]
                        print(one)
                        print(one["proxyport"])
                        print(one["wanIp"])
                        ip = "https://" + one["wanIp"] + ":" + one["proxyport"]
                        self.proxies.drop()
                        self.proxies.insert_one({"proxy": ip})
                        return
            sleep(60)


    def get_random_proxy(self):  
        '''随机从文件中读取proxy'''  
        while(True):
            for proxy in self.proxies.find():
                return proxy['proxy']
            sleep(1)
        


class DynamicProxyMiddleware(object):

    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["Sina"]
        self.proxies = self.db["proxies"]
        self.get()

    def get(self):
        while(True):
            try:
                r = requests.get("http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD20187195466ArkBQ1/c711f5747db611e7bcaf7cd30abda612?returnType=2",
                        timeout=120)
            except Exception as err_info:
                r = None
                print(err_info)

            if r is not None:
                print(r.status_code)
                if r.status_code == 200:
                    print(r.content)
                    print(r.json())
                    result = r.json()
                    if result["ERRORCODE"] == "0" and result["RESULT"]:
                        one = result["RESULT"]
                        print(one)
                        print(one["proxyport"])
                        print(one["wanIp"])
                        ip = "https://" + one["wanIp"] + ":" + one["proxyport"]
                        self.proxies.drop()
                        self.proxies.insert_one({"proxy": ip})
                        return
            sleep(60)

    def get_random_proxy(self):  
        while(True):
            for proxy in self.proxies.find():
                return proxy['proxy']
            sleep(10)

    def process_request(self,request, spider):    
        proxy = self.get_random_proxy()  
        print("DP this is request ip:"+proxy)  
        request.meta['proxy'] = proxy   
  
  
    def process_response(self, request, response, spider):  
        return response  

        

