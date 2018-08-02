#!/usr/bin/env python
# encoding: utf-8
import datetime
import json
import base64
from time import sleep
import requests
import pymongo
    

def proxyfetch():
    client = pymongo.MongoClient("localhost", 27017)
    db = client["Sina"]
    proxies = db["proxies"]
    
    webapi = 'http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=3f6f240befb04a2f9c9b020aed15a2fd&returnType=2&count=1'
    while True:
        proxies.drop()
        try:
            r = requests.get(webapi,timeout=120)
        except Exception as err_info:
            r = None
            print(err_info)

        if r is not None:
            print(r.json())
            result = r.json()

            if result["ERRORCODE"] == "0" and result["RESULT"]:
                res = result["RESULT"]
                new_post = []
                cnt = 0
                for one in res:
                    print(one["ip"],end=':')
                    print(one["port"])
                    ip = "https://" + one["ip"] + ":" + one["port"]
                    new_post.append({"proxy":ip, "cnt":cnt})
                    cnt+=1
                proxies.insert_many(new_post)       
                sleep(15)
            else:
                sleep(15)
        else:
            sleep(15)


proxyfetch()




