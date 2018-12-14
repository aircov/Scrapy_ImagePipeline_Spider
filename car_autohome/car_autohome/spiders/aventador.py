# -*- coding: utf-8 -*-
import scrapy


class AventadorSpider(scrapy.Spider):
    name = 'aventador'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['http://car.autohome.com.cn/']

    def parse(self, response):
        pass
