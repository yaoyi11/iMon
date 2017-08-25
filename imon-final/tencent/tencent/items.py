# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()#链接
    title = scrapy.Field()#标题
    date = scrapy.Field()#抓取时间
    charset = scrapy.Field()#网页编码
    size = scrapy.Field()#网页大小
    domain = scrapy.Field()#域名
    filepath = scrapy.Field()#文件存储路径
    count = scrapy.Field()#每个网页所含连接数
    crawl_id = scrapy.Field()#每个爬虫的id