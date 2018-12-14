# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from car_autohome.items import CarAutohomeItem


class AventadorSpider(CrawlSpider):
    name = 'aventador'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/2277.html']

    rules = (
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/2277-.+'), callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        category = response.xpath("//div[@class='uibox']/div[@class='uibox-title']/text()").get()
        srcs = response.xpath("//div[contains(@class,'uibox-con')]/ul/li//img/@src").getall()

        # 小图url
        # https://car2.autoimg.cn/cardfs/product/g29/M0A/CC/DF/t_autohomecar__ChcCSFuAvBeABRDTAALGlxXVX8M971.jpg
        # 高清大图url
        # https://car2.autoimg.cn/cardfs/product/g29/M0A/CC/DF/autohomecar__ChcCSFuAvBeABRDTAALGlxXVX8M971.jpg

        srcs = list(map(lambda x: response.urljoin(x.replace("t_", "").strip()), srcs))
        # print(srcs)
        yield CarAutohomeItem(category=category, image_urls=srcs)
