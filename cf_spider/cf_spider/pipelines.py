# -*- coding: utf-8 -*-

from pymongo import MongoClient


class CfSpiderPipeline(object):

    def open_spider(self, spider):
        client = MongoClient(host=spider.settings["MONGO_HOST"], port=spider.settings["MONGO_PORT"])
        self.collection = client["qg_ss"]["cf_info"]

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        print("保存成功！")