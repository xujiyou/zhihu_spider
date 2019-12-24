# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pykafka import KafkaClient


class ZhihuSpiderPipeline(object):

    def __init__(self):
        client = KafkaClient(hosts="fueltank-3:9092")
        self.user_detail_producer = client.topics['user_detail'].get_sync_producer()
        self.follower_producer = client.topics['follower'].get_sync_producer()

    def process_item(self, item, spider):
        if item["t"] == "user":
            self.user_detail_producer.produce(bytes(str(item), encoding="utf-8"))
            return item
        elif item["t"] == "follower":
            self.follower_producer.produce(bytes(str(item), encoding="utf-8"))
            return item
