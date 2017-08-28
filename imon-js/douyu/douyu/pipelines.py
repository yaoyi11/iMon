# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class DouyuPipeline(object):
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
        title = item['title']
        lanmu = item['lanmu']
        user = item['user']
        followers = item['followers']
        try:
            self.cursor.execute("INSERT INTO douyu(title,lanmu,user,followers) "
                                "VALUES (%s,%s,%s,%s)" ,(title,lanmu,user,followers))
            self.conn.commit()
            print('数据成功插入！')
        except Exception as e:
            print(e)
        return item
