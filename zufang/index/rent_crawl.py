#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from .rent_mysql import *

import requests
import time
import re
from lxml import etree


def rent_crawl(location):
    rent_obj=Housing_Resources('localhost','root','123456')
    try:
        rent_obj.createDB()
    except Exception:
        print('已经存在库')

    rent_obj.useDB()
    try:
        rent_obj.createTable(location)
    except Exception:
        print('已经存在表%s'%(location))
    
    main()
    rent_obj.enterData(house_title, house_location, house_money, house_url,location)


# 获取某市区域的所有链接
def get_areas(url):
    print('start grabing areas')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    resposne = requests.get(url, headers=headers)
    content = etree.HTML(resposne.text)
    areas = content.xpath("//dd[@data-index = '0']//div[@class='option-list']/a/text()")
    areas_link = content.xpath("//dd[@data-index = '0']//div[@class='option-list']/a/@href")
    for i in range(1,len(areas)):
        area = areas[i]
        area_link = areas_link[i]
        link = 'https://gz.lianjia.com' + area_link
        print('area', area)
        print("开始抓取页面")
        get_pages(area, link, area_link)

#通过获取某一区域的页数，来拼接某一页的链接
def get_pages(area, link, area_link):
    quyu = area_link.split('/')[-2]
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    resposne = requests.get(link, headers=headers)
    pages =  int(re.findall("page-data=\'{\"totalPage\":(\d+),\"curPage\"", resposne.text)[0])
    print("这个区域有" + str(pages) + "页")
    for page in range(1,pages+1):
        url = 'https://gz.lianjia.com/zufang/{}/pg'.format(quyu) + str(page)
        print("开始抓取" + str(page) +"的信息")
        get_house_info(area,url)


#获取某一区域某一页的详细房租信息
def get_house_info(area, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    time.sleep(2)
    try:
        resposne = requests.get(url, headers=headers)
        content = etree.HTML(resposne.text)
        info=[]
        for i in range(30):
            link = content.xpath("//div[@class='info-panel']/h2/a/@href")[i]
            title = content.xpath("//div[@class='where']/a/span/text()")[i]
            # room_type = content.xpath("//div[@class='where']/span[1]/span/text()")[i]
            # square = re.findall("(\d+)",content.xpath("//div[@class='where']/span[2]/text()")[i])[0]
            # position = content.xpath("//div[@class='where']/span[3]/text()")[i].replace(" ", "")
            try:
                detail_place = re.findall("([\u4E00-\u9FA5]+)租房", content.xpath("//div[@class='other']/div/a/text()")[i])[0]
            except Exception as e:
                detail_place = ""
            # floor =re.findall("([\u4E00-\u9FA5]+)\(", content.xpath("//div[@class='other']/div/text()[1]")[i])[0]
            # total_floor = re.findall("(\d+)",content.xpath("//div[@class='other']/div/text()[1]")[i])[0]
            # try:
            #     house_year = re.findall("(\d+)",content.xpath("//div[@class='other']/div/text()[2]")[i])[0]
            # except Exception as e:
            #     house_year = ""
            price = content.xpath("//div[@class='col-3']/div/span/text()")[i]
            # with open('链家广州租房2.txt','a',encoding='utf-8') as f:
            #     f.write(area + ',' + title + ',' + room_type + ',' + square + ',' +position+
            #             ','+ detail_place+','+floor+','+total_floor+','+price+','+house_year+'\n')
            
            print(title, detail_place, price, link)

    except Exception as e:
        print( 'ooops! connecting error, retrying.....', e)
        time.sleep(20)
        return get_house_info(area, url)


def main():
    print('start!')
    url = 'https://gz.lianjia.com/zufang'
    get_areas(url)




# 58同城    有距离
# lianjia
# ziru　　　　　有距离
# leyoujia
# fangtianxia　　有距离









    # url = "http://gz.58.com/pinpaigongyu/pn/{page}/?PGTID={location}"

    # #已完成的页数序号，初时为0
    # page = 0

    # # csv_file = open("rent.csv","w") 
    # # csv_writer = csv.writer(csv_file, delimiter=',')

    # try:
        
           
    #     while True:
    #         page += 1
    #         print("fetch: ", url.format(page=page,location=location))
    #         response = requests.get(url.format(page=page,location=location))
    #         html = BeautifulSoup(response.text, 'lxml')
    #         house_list = html.select(".list > li")

    #         # 循环在读不到新的房源时结束
    #         if not house_list:
    #             break

    #         for house in house_list:
    #             house_title = str(house.select("h2")[0])
    #             house_title_n=house_title[4:][:-5]
    #             house_url = urljoin(url, house.select("a")[0]["href"])
    #             house_info_list = house_title_n.split(" ")
    #             print('house_info_list--->', house_info_list)
    #             for x in house_info_list:
    #                 print(x)
    #             # 如果第二列是公寓名则取第一列作为地址
    #             if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
    #                 house_location = house_info_list[0]
    #             else:
    #                 house_location = house_info_list[1]

    #             house_money = house.select(".money")[0].select("b")[0].string.encode("utf8")
    #             rent_obj.enterData(house_title, house_location, house_money, house_url,location)

          
    # #         csv_writer.writerow([house_title, house_location, house_money, house_url])
    # except Exception as e:
    #     print('已经存在表,不再爬数据', e)

    # # csv_file.close()