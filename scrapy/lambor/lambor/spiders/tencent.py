# # -*- coding: utf-8 -*-
import scrapy
from ..items import LamborItem

class TencentSpider(scrapy.Spider):
    name = "lambor"
    allowed_domains = ["tencent.com"]
    
    url = "http://hr.tencent.com/position.php?&start="
    offset = 0

    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            item = LamborItem()

            item['positionname'] = each.xpath("./td[1]/a/text()").extract()[0]

            item['positionlink'] = each.xpath("./td[1]/a/@href").extract()[0]

            item['positionType'] = each.xpath("./td[2]/text()").extract()[0]

            item['peopleNum'] =  each.xpath("./td[3]/text()").extract()[0]

            item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]

            item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]

            yield item
        if self.offset < 1600:
            self.offset += 10

        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

