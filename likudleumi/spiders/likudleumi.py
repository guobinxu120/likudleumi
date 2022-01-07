# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http import TextResponse, FormRequest
import json, re, csv
from collections import OrderedDict

class WadiSpider(scrapy.Spider):
    name = 'likudleumi'
    # allowed_domains = ['https://likudleumi.org.il/']
    domain = 'https://likudleumi.org.il/'
    start_urls = ['https://likudleumi.org.il/details.php']

    def __init__(self, filename=None, *args, **kwargs):
        super(WadiSpider, self).__init__(*args, **kwargs)

        if not filename:
            raise CloseSpider('Received no filename!')
        else:
            self.filename = filename
            f = open('input/'+filename)
            csv_items = csv.DictReader(f)
            self.numbers = []
            for i, row in enumerate(csv_items):
                self.numbers.append(row['number'])
            f.close()


    def start_requests(self):
        for number in self.numbers:
            yield FormRequest(self.start_urls[0], callback=self.parse, formdata={'id_number': number}, meta={'number': number})

    def parse(self, response):
        if 'Location' in response.headers.keys():
            yield Request(self.domain + response.header['Location'], callback=self.parse, meta={'number': response.meta['number']} )
        result = response.xpath('//*[@id="text2"]/h3/text()').extract_first()
        item = OrderedDict()
        item['number'] = response.meta['number']
        item['result'] = result.encode('utf-8')
        yield item







