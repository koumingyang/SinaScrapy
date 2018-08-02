# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class InformationItem(Item):
    """ 个人信息 """
    _id = Field()  # 用户ID
    NickName = Field()  # 昵称
    Num_Tweets = Field()  # 微博数
    Num_Follows = Field()  # 关注数
    Num_Fans = Field()  # 粉丝数
    URL = Field()  # 首页链接


class TweetsItem(Item):
    """ 微博信息 """
    _id = Field()  # 用户ID-微博ID
    ID = Field()  # 用户ID
    Content = Field()  # 微博内容
    Comment = Field()  # 评论数


class RelationshipsItem(Item):
    """ 用户关系，只保留与关注的关系 """
    fan_id = Field()
    followed_id = Field()  # 被关注者的ID

class CommentItem(Item):
    _id = Field() #tweet id + comment id
    Content = Field() # comment content
    ID = Field() # tweet id
    Like = Field() # subscribe number