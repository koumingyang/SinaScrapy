#!/usr/bin/env python
# encoding: utf-8

import datetime
import requests
import re
from lxml import etree
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from sina.config import weiboID
from sina.items import TweetsItem, InformationItem, RelationshipsItem, CommentItem


class Spider(Spider):
    name = "SinaSpider"
    host = "https://weibo.cn"
    start_urls = list(set(weiboID))

    def start_requests(self):
        for uid in self.start_urls:
            yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_information)

    def parse_information(self, response):
        """ 抓取个人信息 """
        informationItem = InformationItem()
        selector = Selector(response)
        ID = re.findall('(\d+)/info', response.url)[0]
        try:
            text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
            nickname = re.findall('昵称;?[：:]?(.*?);', text1)
            url = re.findall('互联网;?[：:]?(.*?);', text1)


            informationItem["Num_Tweets"] = 0
            informationItem["Num_Follows"] = 0
            informationItem["Num_Fans"] = 0

            informationItem["_id"] = ID
            if nickname and nickname[0]:
                informationItem["NickName"] = nickname[0].replace(u"\xa0", "")
            if url:
                informationItem["URL"] = url[0]

            try:
                urlothers = "https://weibo.cn/attgroup/opening?uid=%s" % ID
                new_ck = {}
                for ck in response.request.cookies:
                    new_ck[ck['name']] = ck['value']
                r = requests.get(urlothers, cookies=new_ck, timeout=5)
                if r.status_code == 200:
                    selector = etree.HTML(r.content)
                    texts = ";".join(selector.xpath('//body//div[@class="tip2"]/a//text()'))
                    if texts:
                        num_tweets = re.findall('微博\[(\d+)\]', texts)
                        num_follows = re.findall('关注\[(\d+)\]', texts)
                        num_fans = re.findall('粉丝\[(\d+)\]', texts)
                        if num_tweets:
                            informationItem["Num_Tweets"] = int(num_tweets[0])
                        if num_follows:
                            informationItem["Num_Follows"] = int(num_follows[0])
                        if num_fans:
                            informationItem["Num_Fans"] = int(num_fans[0])
            except Exception as e:
                pass
        except Exception as e:
            pass
        else:
            yield informationItem
        if informationItem["Num_Tweets"]>0:
            page_cnt = min((informationItem["Num_Tweets"]-1)/10, 2000)
            for i in range(0,int(page_cnt)+1):
                yield Request(url="https://weibo.cn/%s/profile?filter=1&page=%s"%(ID, str(i)),callback=self.parse_tweets,
                          dont_filter=True)

    def parse_comment(self, response):
        """ 打开url爬取里面的comment """
        selector = Selector(response)
       
        tid = re.findall('comment/(\w+)', response.url)[0]
        divs = selector.xpath('body/div[@class="c" and @id]')

        for div in divs:
            try:
                id = div.xpath('@id').extract_first()  # commentID
                if (id[0]=='M'):
                    continue
                commentitem = CommentItem()
                content = div.xpath('span[@class="ctt"]//text()').extract()  # comment内容
                Likes = re.findall('赞\[(\d+)\]', div.extract())  # 赞数
                commentitem["Like"] = 0
                commentitem["_id"] = tid + "-" + id
                commentitem["ID"] = tid

                if content:
                    commentitem["Content"] = " ".join(content).strip('[位置]')  # 去掉最后的"[位置]"
                if Likes:
                    commentitem["Like"] = int(Likes[0])
                yield commentitem
            except Exception as e:
                self.logger.info(e)
                pass
        next_url = selector.xpath('//a[text()="下页"]/@href').extract()
        if next_url:
            yield Request(url=self.host + next_url[0], callback=self.parse_comment, dont_filter=True)

    def parse_tweets(self, response):
        """ 抓取微博数据 """
        selector = Selector(response)
        ID = re.findall('(\d+)/profile', response.url)[0]
        divs = selector.xpath('body/div[@class="c" and @id]')
        for div in divs:
            try:
                tweetsItems = TweetsItem()
                id = div.xpath('@id').extract_first()  # 微博ID

                real_id = id.split('_')[1]

                content = div.xpath('div/span[@class="ctt"]//text()').extract()  # 微博内容
                comment = re.findall('评论\[(\d+)\]', div.extract())  # 评论数
                tweetsItems["Comment"] = 0
                tweetsItems["_id"] = ID + "-" + id
                tweetsItems["ID"] = ID
                if content:
                    tweetsItems["Content"] = " ".join(content).strip('[位置]')  # 去掉最后的"[位置]"
                if comment:
                    tweetsItems["Comment"] = int(comment[0])
                yield tweetsItems

                #enter a tweet
                #https://weibo.cn/comment/ + real_id
                if int(comment[0])>0:
                    yield Request(url="https://weibo.cn/comment/%s" % real_id, callback=self.parse_comment)

            except Exception as e:
                self.logger.info(e)
                pass

        #url_next = selector.xpath('body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="下页"]/@href').extract()
        #if url_next:
        #    yield Request(url=self.host + url_next[0], callback=self.parse_tweets, dont_filter=True)
