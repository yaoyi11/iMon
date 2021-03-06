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
        #过滤http://news.qq.com/a/年月日/后缀为htm的网页
        Rule(LinkExtractor(allow=r"http://news.qq.com/a/201708\d+/\d+\.htm"),callback="parse_item", follow=True),
    )
    link = set()
    domains = set()
    def parse_item(self, response):
        global link,domains
        #self.crawler.settings.get("crawls/somespider-1")
        qqnews = TencentItem()
        try:
            qqnews['url'] = response.url#url地址
            self.link.add(response.url)
            qqnews['title'] = response.xpath('//div[@class="hd"]/h1/text()').extract()#标题
            #时间中的秒数为整数
            qqnews['date'] = str(datetime.now().replace(microsecond=0))#抓取时间
            qqnews['charset'] = response.xpath('/html/head/meta/@charset').extract()[0]#网页编码
            qqnews['size'] = len(response.body)#网页大小
            for site in response.xpath("//a/@href").extract():
                if site not in self.link:#新链接
                    try:
                        n = site.strip().split('/')[2]#提取域名
                        self.domains.add(n)
                    except:
                        pass
                    #self.link.add(site)
            qqnews['domain'] = self.domains
            yield qqnews
        except:
            pass
        for site in Selector(response).xpath('//div[@class="bd"]/ul[@bosszone="jhRE"]'):
            for url in response.selector.xpath("//a/@href").re(r'^http:[a-zA-Z0-9\/\?\=].*'):
                yield scrapy.Request(url, callback=self.parse)
