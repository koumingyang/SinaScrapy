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

from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)

class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):

        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        logger = logging.getLogger(__name__)
        logger.warning('UAM process request')


class CookiesMiddleware(object):
    """ 换Cookie """

    def __init__(self):
        init_cookies()

    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        logger = logging.getLogger(__name__)
        logger.warning('CoM request')
        request.cookies = cookie

class ResponseNotWorkMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):  
        
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["Sina"]
        self.proxies = self.db["proxies"]

        if response.status != 200:  
            logger = logging.getLogger(__name__)
            logger.warning('RN process_response...')
            sleep(10)
            proxy = self.get_random_proxy()  
            logger.warning("RN this is request ip:"+proxy)  
            request.meta['proxy'] = proxy
            request.dont_filter=True
            cookie = random.choice(cookies)
            request.cookies = cookie
            agent = random.choice(agents)
            request.headers["User-Agent"] = agent
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["Sina"]
        self.proxies = self.db["proxies"]
        logger = logging.getLogger(__name__)
        logger.warning('Not Work process_exception...')
        logger.warning(exception)
        sleep(10)
        proxy = self.get_random_proxy()  
        logger.warning("Not Work this is request ip:"+proxy)  
        request.meta['proxy'] = proxy
        request.dont_filter=True
        cookie = random.choice(cookies)
        request.cookies = cookie
        logger.warning('Not Work over!')
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        return self._retry(request, exception, spider)
        

    def get_random_proxy(self):  
        while(True):
            seq = random.randint(0,4)
            if (self.proxies.find_one({'cnt':seq})):
                return self.proxies.find_one({'cnt':seq})['proxy']
            sleep(1)
        


class DynamicProxyMiddleware(object):

    def __init__(self):
        self.maxnumber = 5
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["Sina"]
        self.proxies = self.db["proxies"]


    def get_random_proxy(self):  
        while(True):
            seq = random.randint(0,4)
            if (self.proxies.find_one({'cnt':seq})):
                return self.proxies.find_one({'cnt':seq})['proxy']
            sleep(1)

    def process_request(self,request, spider):    
        proxy = self.get_random_proxy()  
        logger = logging.getLogger(__name__)
        logger.warning("DP this is request ip:"+proxy)  
        request.meta['proxy'] = proxy   
  
  
    def process_response(self, request, response, spider):  
        logger = logging.getLogger(__name__)
        logger.warning("DP response")  
        return response  

        

