# encoding: utf-8
import random
import yaml
from sina.cookies import cookies, init_cookies
from sina.user_agents import agents
from redis import StrictRedis
from time import sleep
import requests

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

class DynamicProxyMiddleware(object):

    def __init__(self):
        pass

    def get(self):
        try:
            r = requests.get("http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD20187195466ArkBQ1/03e20a3d1ddb11e79ff07cd30abda612?returnType=2",
                    timeout=120)
        except Exception as err_info:
            r = None
            print(err_info)

        with open('/home/kmy/WeiboSpider-master/proxies.txt', 'w') as f:
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
                        ip = "https://" + one["wanIp"] + ":" + one["proxyport"] + "\n"
                        f.write(ip)

    def process_request(self,request, spider):  
        '''对request对象加上proxy'''  
        proxy = self.get_random_proxy()  
        print("this is request ip:"+proxy)  
        request.meta['proxy'] = proxy   
  
  
    def process_response(self, request, response, spider):  
        '''对返回的response处理'''  
        # 如果返回的response状态不是200，重新生成当前request对象  
        if response.status != 200:  
            print("Dynamic response")
            self.get()
            sleep(2)

            proxy = self.get_random_proxy()  
            print("this is response ip:"+proxy)  
            # 对当前reque加上代理  
            request.meta['proxy'] = proxy   
            return request  
        return response  
  
    def get_random_proxy(self):  
        '''随机从文件中读取proxy'''  
        while 1:  
            with open('/home/kmy/WeiboSpider-master/proxies.txt', 'r') as f:  
                proxies = f.readlines()  
            if proxies:  
                break  
            else:  
                time.sleep(1)  
        proxy = random.choice(proxies).strip()  
        return proxy
        

