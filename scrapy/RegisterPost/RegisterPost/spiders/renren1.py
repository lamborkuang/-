# -*- coding: utf-8 -*-
import scrapy


class Renren1Spider(scrapy.Spider):
    name = "renren1"
    allowed_domains = ["renren.com"]
    # start_urls = (
    #     'http://www.renren.com/PLogin.do',
    # )

    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'
        yield scrapy.FormRequest(url=url, formdata={'emain':'455832655@qq.com', 'password':'ksz2791225'},
            callback= self.parse)

    def parse(self, response):
        with open('renren1.html', 'w') as f:
            f.write(response.body)
            
