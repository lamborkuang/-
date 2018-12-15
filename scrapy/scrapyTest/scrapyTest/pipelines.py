# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ScrapytestPipeline(object):
    def process_item(self, item, spider):
        
        with open('tencent.json', 'ab') as f:
            text = json.dumps(dict(item), ensure_ascii=False) + '\n'
            f.write(text.encode('utf8')) 

        return item
