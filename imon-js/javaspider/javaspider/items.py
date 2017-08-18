# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JavaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    daima = scrapy.Field()#代码
    name = scrapy.Field()#名称
    latest_price = scrapy.Field()#最新价
    zhangdie = scrapy.Field()#涨跌额
    zhangdiefu = scrapy.Field()#涨跌幅
    buy_in = scrapy.Field()#买入
    sell_out = scrapy.Field()#卖出
    yesterday = scrapy.Field()#昨收
    today = scrapy.Field()#今开
    high = scrapy.Field()#最高
    low = scrapy.Field()#最低
    dillcount = scrapy.Field()#成交量（手）
    dillmon = scrapy.Field()#成交额（万）

