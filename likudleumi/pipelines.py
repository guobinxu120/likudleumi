# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import os, csv

class LikudleumiPipeline(object):
    def __init__(self):
            #Instantiate API Connection
        self.filewirter = None
        self.file = None


    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline


    def spider_opened(self, spider):
        filename = spider.filename
        filename = "output/" + os.path.splitext(filename)[0] + "_output" + os.path.splitext(filename)[1]
        self.file = open(filename,"wb")
        self.filewirter = csv.writer(self.file, delimiter=',',quoting=csv.QUOTE_ALL)
        self.filewirter.writerow(["number", "result"])

    def spider_closed(self, spider):
        if self.file != None:
            self.file.close()

    def process_item(self, item, spider):
        self.filewirter.writerow(item.values())
        return item
