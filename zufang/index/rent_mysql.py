#coding = utf8
'''

本程序的功能是
    1.创建数据库,创建一定格式的表格 type addr price url  2.把数据传入数据库  3.根据条件查找数据(price_min price_max)  4.返回获取的数据(列表)

'''


import pymysql




class Housing_Resources():
    def __init__(self,IP,uesrName,password,information_schema = 'information_schema'):
        '''类被调用的时候 
        1.开始连接数据库,创建游标
        2.传入需要查找的信息的条件'''

        self.db = pymysql.connect(IP,uesrName,password,information_schema,charset="utf8")
        self.cur = self.db.cursor()
        # self.DBname = Housing_resources
        # self.addr = addr
        # self.price = price

    def createDB(self):
        '''创建库,并且创建一定格式的表'''

        create_Order = 'create database houseDB;'
        self.cur.execute(create_Order)

    def useDB(self):
        self.cur.execute('use houseDB;')

    def createTable(self,location):
        self.cur.execute('create table if not exists {} (type varchar(1000),addr varchar(1000),price varchar(100),url varchar(1000),index(price),unique(url))default charset=utf8;'.format(location))

    # def show_tables(self, location):
    #     try:
    #         showtb = self.cur.execute('select * from {};'.format(location))
    #         print('showtb', showtb)
            
    #     except Exception as e:
    #         print(e)

    def enterData(self,house_title, house_location, house_money, house_url,location):
        '''储存房源信息到数据库'''

        # f = open('./rent.csv')
        # while True:
        #     data = f.readline()
        #     print(data)

        #     if not data:
        #         break
                
            # data.split(',')
            # print(data.split(','))
            # dataline = data.split(',')
        insertdata = "insert into {} values('{}','{}','{}','{}');".format(location,house_title[4:-5], house_location, str(house_money)[2:-1], house_url)
        print(insertdata)
        self.cur.execute(insertdata)
        self.db.commit()
        # f.close()

    def handleData(self,price_min,price_max):
        '''数据转换,用于方便在查找数据库数据 转换后 返回 self.price_min 和 self.price_maxe'''

        self.price_min = int(price_min[0])
        self.price_max = int(price_max[0])


    def getDataByPrice(self,location):
        '''用转换后的数据self.price_min 和 self.price_max 来获取对应的数据,返回搜索到的信息 self.alltrue_data'''

        # self.cur.execute('use {}'.format(DBname))
        self.alltrue_data = []
        if self.price_min < self.price_max:
            for i in range(self.price_min,self.price_max+1):
                # print('查找',i)
                selectdata = "select * from {} where  price regexp '^{}.+';".format(location,str(i))
                self.cur.execute(selectdata)
                self.db.commit()

                self.getdata = self.cur.fetchall()
        #返回一个元组,每一个元素也是一个元组,每一个元素就是符合条件的一条记录

                self.alltrue_data.append(self.getdata)
        #用列表收集符合要求的数据，列表的原元素是元组（符合一个价位的所有信息））

        elif self.price_min > self.price_max:
            for i in range(self.price_max+1,self.price_min):
                selectdata = "select * from {} where  price regexp '^{}.+';".format(location,str(i))
                self.cur.execute(selectdata)
                self.getdata = self.cur.fetchall()
                self.alltrue_data.append(self.getdata)



        elif self.price_min == self.price_max:
            selectdata = "select * from {} where  price regexp '^{}.+';".format(location,str(self.price_min))
            self.cur.execute(selectdata)
            self.getdata = self.cur.fetchall()  
            self.alltrue_data.append(self.getdata)


        # print(self.alltrue_data)


    def regetData(self):
        '''将每一条符合要求的记录转换成用列表的形式，并返回'''


        allgettrue_data = []
        for i in self.alltrue_data:
            #一个价格有多少条符合的信息
            for j in i:
                onedata = []
                for k in j:
                    onedata.append(k)
                allgettrue_data.append(onedata)

        if  not allgettrue_data:
            return('1')
        else:
            return allgettrue_data

    def closeDB(self):
        self.cur.close()
        self.db.close()




#下面程序用于自测

# def main():
#     test = Housing_Resources('localhost','root','123456')
#     # test.createDB_Table('testdbname')
#     # test.enterData()
#     test.handleData('7','9')
#     test.getDataByPrice('testdbname')
#     print(test.regetData())
#     test.closeDB()








# if __name__ == "__main__":
#     main()






