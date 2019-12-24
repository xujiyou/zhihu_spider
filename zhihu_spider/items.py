# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserDetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    t = scrapy.Field()
    url_token = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    major = scrapy.Field()
    company = scrapy.Field()
    occupation = scrapy.Field()
    university = scrapy.Field()
    tie = scrapy.Field()
    pass


class FollowerItem(scrapy.Item):
    t = scrapy.Field()
    v = scrapy.Field()
    id = scrapy.Field()
    url_token = scrapy.Field()
    name = scrapy.Field()
    use_default_avatar = scrapy.Field()
    avatar_url = scrapy.Field()
    avatar_url_template = scrapy.Field()
    is_org = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
    user_type = scrapy.Field()
    headline = scrapy.Field()
    gender = scrapy.Field()
    is_advertiser = scrapy.Field()
    vip_info = scrapy.Field()
    pass
