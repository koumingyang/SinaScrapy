#!/usr/bin/env python
# encoding: utf-8
import datetime
import json
import base64
from time import sleep

import pymongo

cookie = "SINAGLOBAL=7766568440221.359.1530281366100; wb_view_log=1536*8641.25; wb_view_log_5770926079=1536*8641.25; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; _s_tentry=-; appkey=; Apache=1995353314740.791.1531912755075; ULV=1531912755086:3:2:2:1995353314740.791.1531912755075:1531892257611; login_sid_t=9d69f4a29d4e739fb8969e3c27be597c; cross_origin_proto=SSL; YF-V5-G0=a9b587b1791ab233f24db4e09dad383c; WBStorage=5548c0baa42e6f3d|undefined; UOR=www.jirou.com,widget.weibo.com,login.sina.com.cn; un=neifutang7616@163.com; wb_view_log_6597811383=1536*8641.25; YF-Page-G0=d30fd7265234f674761ebc75febc3a9f; WBtopGlobal_register_version=2018071819; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5abAl0raQH0THjBgUDpAqa5JpX5K2hUgL.Foqf1KMReK201he2dJLoI0zLxK-LBKBL1-2LxKqLB-BLBKBLxKBLBonL1h5LxKML1hnLBo2LxKnL1K-LB.Hk-.vKxBtt; ALF=1563448916; SSOLoginState=1531912917; SCF=Am1yc4DfEqUgJR5DW8BAXVccF4CyztVahi4lk_wTcfLsOCo_m0EcVDern-_6wV7dwmN5lhq5WB3IRdGhH7W4jmo.; SUB=_2A252S1KGDeRhGeBL4lUZ8S_Pwz-IHXVVIcNOrDV8PUNbmtBeLUr3kW9NRq-22BVCh7AuVEdmY6d7GWJPz7sDuUwl; SUHB=0oU4u4S2Ed-f0t; wvr=6"
account = "neifutang7616@163.com"

client = pymongo.MongoClient("localhost", 27017)
db = client["Sina"]
userAccount = db["userAccount"]

if __name__ == "__main__":
    try:
        userAccount.drop()
    except Exception as e:
        pass
        
    userAccount.insert_one({"_id": account, "cookie": cookie})