# from scrapy import cmdline
#
# cmd = 'scrapy crawl qqnews'
# cmdline.execute(cmd.split(' '))
# -*- coding: utf-8 -*-
import codecs
import os
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule, CrawlSpider
from scrapy.utils.project import get_project_settings

from tencent.items import TencentItem

link = set()
domains = set()
class MySpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, *args, **kwargs):
        self.start_urls = kwargs.pop('url_list',[])
        self.allowed_domains = self.start_urls[0].strip().split('/')[2]
        print(self.start_urls[0].strip().split('/'))
        print(self.allowed_domains)
        # self._rules = (
        # #过滤http://news.qq.com/a/年月日/后缀为htm的网页
        # #Rule(
        #     Rule(LinkExtractor(allow=r'http://news.qq.com/a/201708\d+/\d+\.htm'),callback="parse_item", follow=True),
        # )
        super(MySpider, *args, **kwargs)

    def parse(self, response):
        print("1111")
        global link, domains
        # print(response.request.url)
        # print(len(response.body))
        qqnews = TencentItem()
        #print(response.url)
        try:
            qqnews['url'] = response.url#url地址
            self.link.add(response.url)
            title= response.xpath('//div[@class="hd"]/h1/text()').extract()#标题
            qqnews['title'] =title
            #时间中的秒数为整数
            qqnews['date'] = str(datetime.now().replace(microsecond=0))#抓取时间
            charset= response.xpath('/html/head/meta/@charset').extract()[0]#网页编码
            qqnews['charset'] = charset
            qqnews['size'] = len(response.body)#网页大小
            filename = "D:\\testFile\\html\\" + str(title[0]) + '.txt'
            fp = codecs.open(filename, "w+", charset)  # 保存在文件夹下
            content = response.body.decode(charset, 'ignore')
            fp.write(content)
            fp.close()
            qqnews['filepath'] = filename
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
        for url in response.selector.xpath("//a/@href").re(r"http://news.qq.com/a/201708\d+/\d+\.htm"):
            print(url)
            yield scrapy.Request(url, callback=self.parse)#在这里出错，它根本没有运行这句话
#配置文件
sett = get_project_settings()
sett['DOWNLOAD_DELAY'] = 1
sett['USER_AGENT'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.13 Safari/537.36'
sett['DEPTH_PRIORITY'] = 2
#sett['SCHEDULER_ORDER'] = 'DFO'
#print(sett)

process = CrawlerProcess(sett)

process.crawl(MySpider, url_list = ['http://news.qq.com/'])
process.start()