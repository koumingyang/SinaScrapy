#!/usr/bin/env python
# encoding: utf-8
import datetime
import json
import base64
from time import sleep
import requests

def get():

    try:
        r = requests.get("http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD20187195466ArkBQ1/03e20a3d1ddb11e79ff07cd30abda612?returnType=2",
                timeout=120)
    except Exception as err_info:
        r = None
        print(err_info)

    with open('proxies.txt', 'w') as f:
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
    

while(True):             
    get() 
    sleep(300)   
    