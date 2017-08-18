# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class JavaspiderPipeline(object):
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
        daima = item['daima']
        name = item['name']
        latest_price = item['latest_price']
        zhangdie = item['zhangdie']
        zhangdiefu = item['zhangdiefu']
        buy_in = item['buy_in']
        sell_out = item['sell_out']
        yesterday = item['yesterday']
        today = item['today']
        high = item['high']
        low = item['low']
        dillcount = item['dillcount']
        dillmon = item['dillmon']
        try:
            self.cursor.execute("INSERT INTO sina(daima,name,latest_price,zhangdie,zhangdiefu,buy_in,sell_out,yesterday,today,high,low,dillcount,dillmoney) "
                                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" ,(daima,name,latest_price,zhangdie,zhangdiefu,buy_in,sell_out,yesterday,today,high,low,dillcount,dillmon))
            self.conn.commit()
            print('数据成功插入！')
        except Exception as e:
            print(e)

        return item
