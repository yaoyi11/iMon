# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import os
import pymysql
from tencent.items import TencentItem
from scrapy.exceptions import DropItem

class TencentPipeline(object):
    def __init__(self):
        # 和本地的newsDB数据库建立连接
        self.conn = pymysql.connect(
            host='localhost',  # 连接的是本地数据库
            user='root',  # mysql用户名
            passwd=None,  # 密码
            db='first',  # 数据库的名字
            charset='utf8')  # 默认的编码方式：
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        url = item['url']
        title = item['title']
        date = item['date']
        charset = item['charset']
        size = item['size']
        domain = item['domain']

        try:
            self.cursor.execute("INSERT INTO pages(url,title,date,charset,size) VALUES (%s,%s,%s,%s,%s)" ,(url,title,date,charset,size))
            num = self.cursor.execute("select LAST_INSERT_ID() from pages")
            num = int(num)
            for i in domain:
                self.cursor.execute("INSERT INTO url(page_id,domains) VALUES (%d,'%s')" % (num,i))
                self.conn.commit()
            self.conn.commit()
            print('数据成功插入！')
        except Exception as e:
            print(e)
            print("没有插入")
        finally:
            print("已存入数据库的网页数量是："+str(self.cursor.execute("select LAST_INSERT_ID() from pages")))
            self.cursor.execute("select max(size) from pages")
            max = self.cursor.fetchone()[0]
            self.cursor.execute("select min(size) from pages")
            min = self.cursor.fetchone()[0]
            # lim = max-min
            # avg = lim/10
            # avg = int(avg+1)
            # g = []
            # for i in range(11):
            #     g.append(min+avg*i)
            # for i in range(11):
            #     print(g[i])
            #     # if i<9:
            #     #     self.cursor.execute("select count(*) from pages where (size>='{$g[i]}' and size <'{$g[i+1]}')")
            #     #     print(self.cursor.fetchone()[0])
            print("网页最大："+str(max)+"  网页最小："+str(min))
            #self.cursor.execute("select distinct domains from url")
            #print(self.cursor.fetchone())
            #self.cursor.close()
            #self.conn.close()
        return item
