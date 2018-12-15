# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PicturePipeline(object):
    def __init__(self):
        self.file = open('picture.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)


        return item

    def close_spider(self):
        self.file.close()
