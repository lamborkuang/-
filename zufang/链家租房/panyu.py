
import requests
import time
import re
from lxml import etree



def get_pages():
    url = 'https://gz.lianjia.com/ershoufang/panyu/pg1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    resposne = requests.get(url, headers=headers)
    content = etree.HTML(resposne.text)

    pages = int(content.xpath('//div[@class="resultDes clear"]/h2[@class="total fl"]/span/text()')[0])//30 + 1
    
    print( "这个区域有" + str(pages) + "页")
    for i in range(1, pages+1):
        
        link = 'https://gz.lianjia.com/ershoufang/panyu/pg' + str(i)
        print("开始抓取第" + str(i) +"页的信息", link)
        get_house_info(link)
        print("已经抓取完了第" + str(i) +"页的信息!!!!!!")


def get_house_info(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    time.sleep(0.2)
    
    try:
        resposne = requests.get(link, headers=headers)
        content = etree.HTML(resposne.text)
        info=[]
        print('content------->', content)
        for i in range(30):
            # print('kaishi ', i)
            title = content.xpath("//div[@class='info clear']//div[@class='title']/a/text()")[i]
            houseIcon = content.xpath("//div[@class='info clear']//div[@class='address']/div[@class='houseInfo']/a/text()")[i]
            houseInfo = content.xpath("//div[@class='info clear']//div[@class='address']/div[@class='houseInfo']/text()")[i]
            positionIcon = content.xpath("//div[@class='info clear']//div[@class='flood']/div[@class='positionInfo']/text()")[i]
            followInfo = content.xpath("//div[@class='info clear']//div[@class='followInfo']/text()")[i]
            try:
                tags = content.xpath("//div[@class='info clear']//div[@class='tag']/text()")[i]
            except:
                tags = ''

            priceInfo = content.xpath("//div[@class='info clear']//div[@class='priceInfo']/div[@class='totalPrice']/span/text()")[i] + '万'
            unitPrice = content.xpath("//div[@class='info clear']//div[@class='priceInfo']/div[@class='unitPrice']/span/text()")[i]

            try:
            	image = content.xpath('//li[@class="clear LOGCLICKDATA"]/a[@class="noresultRecommend img "]/img[@class="lj-lazy"]/@src')[i]
            except:
            	image = ''
            # print(title, houseIcon, houseInfo, positionIcon,followInfo, tags, priceInfo, unitPrice)
            print(title, houseIcon, houseInfo, positionIcon,followInfo, tags, priceInfo, unitPrice)
            with open('链家番禺二手房价text.txt','a',encoding='utf-8') as f:
            	f.write(priceInfo +','+ unitPrice +','+title + ',' + houseIcon+
						','+ houseInfo +','+ positionIcon +','+ followInfo + ',' + tags +'\n')
            	

    except Exception as e:
        print('e----->', e)
        return
       

def main():
    print('start!')
    
    get_pages()



if __name__ == '__main__':
    main()