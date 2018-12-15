

import scrapy

from ..items import ScrapytestItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']

    start_urls =  'https://hr.tencent.com/position.php?&start='

    def parse(self, response):

        for each in response.xpath("//tr[@class='even']|//tr[@class='odd']"):
            item = ScrapytestItem()
            item['positionName'] = each.xpath('./td[1]/a/text()').extract()[0]
            item['positionLink'] = "https://hr.tencent.com/" + each.xpath('./td[1]/a/@href').extract()[0]
            item['positionType'] = each.xpath('./td[2]/text()').extract()[0]
            yield item


        nextUrl = response.xpath('//*[@id="next"]/@href').extract()[0]

        yield scrapy.Request("https://hr.tencent.com/"+nextUrl, callback=slef.parse)


