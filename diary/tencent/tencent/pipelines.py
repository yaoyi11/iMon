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
        filepath = item['filepath']

        try:
            #单个网页的url，标题，抓取时间，编码，大小插入到数据表pages
            self.cursor.execute("INSERT INTO page(url,title,date,charset,size,filepath) VALUES (%s,%s,%s,%s,%s,%s)" ,(url,title,date,charset,size,filepath))
            #获取最后插入的id
            num = self.cursor.execute("select LAST_INSERT_ID() from page")
            num = int(num)
            for i in domain:
                #将单个网页里所有的外部域名插入到url表
                self.cursor.execute("INSERT INTO url(page_id,url,domains) VALUES (%d, '%s','%s')" % (num,url,i))
                self.conn.commit()
            self.conn.commit()
            print('数据成功插入！')
        except Exception as e:
            print(e)
            print("没有插入")

        return item
