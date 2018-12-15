# -*- coding: utf-8 -*-
import scrapy
from Top250.items import Top250Item

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    # start_urls = (
    #     'https://movie.douban.com/top250?start=',
    # )
    start = 0
    end = '&filter='
    url = 'https://movie.douban.com/top250?start='
    start_urls = [ url + str(start) + end]


    def parse(self, response):
        item = Top250Item()
        try:
            # movies = response.xpath('//[@class="info"]').extract()
            movies = response.xpath('//div[@class="info"]')
            print(movies)
            for each in movies:
                title = each.xpath('./div[@class="hd"]/a/text()').extract()

                content = each.xpath('./div[@class="bd"]/p[1]/text()').extract()

                score = each.xpath('./div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()

                info = each.xpath('./div[@class="bd"]/p[@class="quote"]/text()').extract()

                item['title'] = title[0]
                item['content'] = ';'.join(content)
                item['score'] = score[0]
                item['info'] = info[0]
                print('item', item)

                yield item

            if self.start <= 225:
                self.start += 25

                yield scrapy.Request(self.url+str(self.start) + self.end, callback=self.parse)
        except:
            pass
