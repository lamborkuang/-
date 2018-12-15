# -*- coding: utf-8 -*-
import scrapy
import re

class DeskSpider(scrapy.Spider):
    name = "desk"
    allowed_domains = ["desk.zol.com.cn"]
    start_urls = [
        'http://desk.zol.com.cn/fengjing/1920x1080/1.html',
    ]

    def parse(self, response):
        print('response', response)
        li = response.xpath('//ul[@class="pic-list2  clearfix"]/li')
        print('li-------->',li)

        for each in range(len(li)):
            pic = response.xpath('//ul[@class="pic-list2  clearfix"]/li[%d]/a/img/@src'%each)
            title = response.xpath('//ul[@class="pic-list2  clearfix"]/li[%d]/a/img/@src'%each)
            print(pic, title)


