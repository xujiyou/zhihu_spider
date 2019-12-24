# -*- coding: utf-8 -*-
import scrapy
import json


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.zhihu.com/people/excited-vczh/followers', callback=self.parse)
        yield scrapy.Request(url='https://www.zhihu.com/api/v4/members/excited-vczh/followees?limit=20', callback=self.parse_follower)

    def parse(self, response):
        url_token = response.url.split("/people/")[1].split("/followers")[0]
        # 先获取用户基本信息
        name = response.css(".ProfileHeader-name ::text").get()
        desc = response.css(".ProfileHeader-headline ::text").get()

        info_class = response.css(".ProfileHeader-info")
        one_item_div = info_class.css(".ProfileHeader-infoItem:first-child")
        two_item_div = info_class.css(".ProfileHeader-infoItem:last-child")
        one_item_div_text_list = one_item_div.xpath("text()")
        two_item_div_text_list = two_item_div.xpath("text()")
        major = ""
        company = ""
        occupation = ""
        university = ""
        tie = ""
        if len(one_item_div_text_list) >= 1:
            major = one_item_div_text_list[0].get()
        if len(one_item_div_text_list) >= 2:
            company = one_item_div_text_list[1].get()
        if len(one_item_div_text_list) >= 3:
            occupation = one_item_div_text_list[2].get()

        if len(info_class.css(".ProfileHeader-infoItem")) == 2:
            if len(two_item_div_text_list) >= 1:
                university = two_item_div_text_list[0].get()
            if len(two_item_div_text_list) >= 2:
                tie = two_item_div_text_list[1].get()

        item = {
            "t": "user",
            "url_token": url_token,
            "name": name,
            "desc": desc,
            "major": major,
            "company": company,
            "occupation": occupation,
            "university": university,
            "tie": tie,
        }
        yield item

    def parse_follower(self, response):
        json_obj = json.loads(response.body_as_unicode())
        is_end = json_obj["paging"]["is_end"]
        next_url = json_obj["paging"]["next"]
        data = json_obj["data"]
        for follower_obj in data:
            # 记录关注者信息，并获取更多信息
            follower_obj["t"] = "follower"
            follower_obj["v"] = response.url.split("/members/")[1].split("/followees")[0]
            yield follower_obj
            yield scrapy.Request(url=follower_obj["url"] + '/followers', callback=self.parse)

        if not is_end:
            # 分页获取关注着列表
            yield scrapy.Request(
                url="https://www.zhihu.com/api/v4/members/excited-vczh/followees?" + next_url.split("?")[1],
                callback=self.parse_follower
            )

        # 迭代获取用户关注者列表
        for follower_obj in data:
            yield scrapy.Request(url='https://www.zhihu.com/api/v4/members/' + follower_obj["url_token"] + '/followees?limit=20',
                                 callback=self.parse_follower)
