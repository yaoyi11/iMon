# -*- coding: utf-8 -*-
import logging
import scrapy
from scrapy import Request
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from tencent.items import TencentItem
from datetime import datetime

class qqnews(CrawlSpider):
    name = "qqnews"  # 爬虫名字
    allowed_domains = ["qq.com"]  # 域名限制
    download_delay = 1
    start_urls = ["http://news.qq.com/"]
    rules = (
        Rule(LinkExtractor(allow=r"http://*"),callback="parse_fen",follow=True),
        Rule(LinkExtractor(allow=r"http://news.qq.com/a/201708\d+/\d+\.htm"),callback="parse_item", follow=True),
    )
    # baseurl = 'http://news.qq.com/a/20170801/'
    # add = '031607'
    # url = baseurl+add+'.htm'
    # start_urls.append(url)

    def parse_item(self, response):
        self.crawler.settings.get("crawls/somespider-1")
        qqnews = TencentItem()
        #print(response.url)
        try:
            qqnews['url'] = response.url#url地址
            qqnews['title'] = response.xpath('//html/head/title/text()').extract()#标题
            #时间中的秒数为整数
            qqnews['date'] = str(datetime.now().replace(microsecond=0))#抓取时间
            qqnews['charset'] = response.xpath('/html/head/meta/@charset').extract()[0]#网页编码
            qqnews['size'] = len(response.body)#网页大小
            yield qqnews
        except:
            pass
        n = response.url.strip().split('/')[-1][:-4]
        #print(n)
        for site in Selector(response).xpath('//div[@class="bd"]/ul[@bosszone="jhRE"]'):
            #qqnews['url'] = site.xpath('.//li/a/@href').extract()
            #qqnews['title'] = site.xpath('.//span[@class="txt"]/text()').extract()
            #yield qqnews
            for url in response.selector.xpath("//a/@href").re(r'^http://news.qq.com/*'):
                yield scrapy.Request(url, callback=self.parse)

    def parse_fen(self, response):
        qqnews = TencentItem()

        for url in response.selector.xpath("//a/@href"):
            qqnews['links'] = url
            yield qqnews
            print(qqnews['links'])
            yield scrapy.Request(url, callback=self.parse)
