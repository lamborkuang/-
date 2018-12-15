
import requests
import time
import re
from lxml import etree

def get_areas(url):
    print('start grabing areas')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    resposne = requests.get(url, headers=headers)
    content = etree.HTML(resposne.text)
    areas_ch = content.xpath("//div[@class = 'filter-by-area-container']//ul[@class='district-wrapper']/li/text()")
    areas_en = content.xpath("//div[@class = 'filter-by-area-container']//ul[@class='district-wrapper']/li/@data-district-spell")
    
    # areas_link = content.xpath("//dd[@data-index = '0']//div[@class='option-list']/a/@href")
    for i in range(0,len(areas_en)):
        area = areas_en[i]
      
        get_pages(area)

def get_pages(area):
    url = 'https://gz.fang.lianjia.com/loupan/'+ area +'/pg'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    resposne = requests.get(url, headers=headers)
    content = etree.HTML(resposne.text)

    pages = int(content.xpath('//div[@class="resblock-have-find"]/span[@class="value"]/text()')[0])//4 + 1
    
    print(area + "这个区域有" + str(pages) + "页")
    for i in range(1, pages+1):
        print('i------>', i)
        link = 'https://gz.fang.lianjia.com/loupan/'+ area +'/pg' + str(i)
        print("开始抓取第" + str(i) +"页的信息", link)
        get_house_info(link)
        print("已经抓取完了第" + str(i) +"页的信息!!!!!!")


def get_house_info(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    time.sleep(1)
    
    try:
        resposne = requests.get(link, headers=headers)
        content = etree.HTML(resposne.text)
        info=[]
        print('content------->', content)
        for i in range(10):
            # print('kaishi ', i)
            title = content.xpath("//div[@class='resblock-desc-wrapper']//div[@class='resblock-name']/a/text()")[i]
            room_type = content.xpath("//div[@class='resblock-desc-wrapper']//div[@class='resblock-name']/span[@class='resblock-type']/text()")[i]
            status = content.xpath("//div[@class='resblock-desc-wrapper']//div[@class='resblock-name']/span[@class='sale-status']/text()")[i]
           

            qu = content.xpath("//div[@class='resblock-desc-wrapper']//div[@class='resblock-location']/span[1]/text()")[i]
            zhen = content.xpath("//div[@class='resblock-desc-wrapper']//div[@class='resblock-location']/span[2]/text()")[i]
            loca = content.xpath("//div[@class='resblock-desc-wrapper']//div[@class='resblock-location']/a/text()")[i]
            
            try:
            	square = content.xpath("//div[@class='resblock-desc-wrapper']//div[@class='resblock-area']/span/text()")[i]
            except:
            	square = ''
            price = content.xpath("//div[@class='resblock-desc-wrapper']//div[@class='resblock-price']/div[@class='main-price']/span[@class='number']/text()")[i]
            try:
            	zongjia = content.xpath("//div[@class='resblock-desc-wrapper']//div[@class='resblock-price']/div[@class='second']/text()")[i]
            except:
            	zongjia = ''
            # print(title, room_type, status, price, square)
            try:
            	image = content.xpath('//li[@class="resblock-list"]/a[@class="resblock-img-wrapper"]/text()')[i]
            except:
            	image = ''
            print(title, room_type, status,  square, qu, zhen, loca, price, zongjia, image)
            with open('链家广州新房房价.txt','a',encoding='utf-8') as f:
            	f.write(price+','+zongjia+','+title + ',' + qu+
						','+ zhen+','+loca+','+ room_type + ',' + status + ',' + square + ',' +image+'\n')
            	# f.write(0, title)
            	# f.write(1, room_type)
            	# f.write(2, status)
            	# f.write(3, square)
            	# f.write(4, qu)
            	# f.write(5, zhen)
            	# f.write(6, loca)
            	# f.write(7, price)
            	# f.write(8, zongjia)
            	# f.write(9, image)
            	# f,write('\n')


    except Exception as e:
        print('e----->', e)
        return
       

def main():
    print('start!')
    url = 'https://gz.fang.lianjia.com/loupan/'
    get_areas(url)



if __name__ == '__main__':
    main()

