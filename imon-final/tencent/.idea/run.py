# -*- coding: utf-8 -*-
import codecs
import os
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
import scrapy
from scrapy import Request, crawler
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule, CrawlSpider
from scrapy.utils.project import get_project_settings
import pymysql

from tencent.items import TencentItem
import getopt
import sys

class MySpider(scrapy.Spider):
    name = 'myspider'
    links = set()
    domains = set()
    def __init__(self, *args, **kwargs):
        self.start_urls = kwargs.pop('url_list',[])
        domain = self.start_urls[0].strip().split('/')[2]
        #print(self.start_urls[0].strip().split('/'))
        self.allowd_domains = []
        self.allowd_domains.append(domain)
        #print(self.allowd_domains)
        super(MySpider, *args, **kwargs)

    def parse(self, response):
        global links, domains
        # print(response.request.url)
        # print(len(response.body))
        qqnews = TencentItem()
        setting = get_project_settings()
        print(setting['DOWNLOAD_DELAY'])
        #print(response.url)
        try:
            meta = response.meta
            print(meta)
            qqnews['url'] = response.url#url地址
            self.links.add(response.url)
            title= response.xpath('//html/head/title/text()').extract()#标题
            qqnews['title'] =title
            #时间中的秒数为整数
            qqnews['date'] = str(datetime.now().replace(microsecond=0))#抓取时间
            #charset= response.xpath('/html/head/meta/@charset').extract()[0]#网页编码
            charset = response.encoding
            qqnews['charset'] = charset
            qqnews['size'] = len(response.body)#网页大小
            filename = "D:\\testFile\\html\\" + str(title[0]) + '.txt'
            fp = codecs.open(filename, "w+", charset)  # 保存在文件夹下
            content = response.body.decode(charset, 'ignore')
            fp.write(content)
            fp.close()
            qqnews['filepath'] = filename
            for site in response.xpath("//a/@href").re(r'^http[s]{0,1}:[a-zA-Z0-9\/\?\=].*'):
                if site not in self.links:#新链接
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
        #print(self.allowd_domains[0])
        if meta['depth']<2:
            for url in response.selector.xpath("//a/@href").re(r'^http[s]{0,1}://%s/[a-zA-Z0-9\/\?\=].*' % self.allowd_domains[0]):
                print(url)
            # print("222222")
                yield scrapy.Request(url, callback=self.parse )#在这里出错，它根本没有运行这句话
        else:
            process.stop()

def get_crawl(url, order, date1, date2):
    try:
        conn = pymysql.connect(
            host='localhost',  # 连接的是本地数据库
            user='root',  # mysql用户名
            passwd=None,  # 密码
            db='first',  # 数据库的名字
            charset='utf8')  # 默认的编码方式：
    except Exception as e:
        print(e)
    cursor = conn.cursor()
    date = datetime.now().replace(microsecond=0)
    site = url[0]
    order = order
    start_time = date1
    end_time = date2
    sql = "INSERT INTO crawl(url,`order`,start_time,end_time) VALUES ('%s', '%s',\'%s\', \'%s\')" % (site, order, start_time, end_time)
    cursor.execute(sql)

    conn.commit()
    print("eeeeeeeeeeeeeeee")

#配置文件
config = {
    "url": "http://news.sina.com.cn/",
    "order": "DFO",
    "depth": "3",
    "delay": "2",
    "crawl_id": "1"
}

# getopt三个选项，第一个一般为sys.argv[1:],第二个参数为短参数，如果参数后面必须跟值，须加:，第三个参数为长参数
opts, args = getopt.getopt(sys.argv[1:], 'hu:o:d:e:c:',
                           [
                               'url=',
                               'order=',
                               'help',
                               'depth=',
                               'delay=',
                               'crawl_id='
                           ]
                           )

# 参数的解析过程,长参数为--，短参数为-
for option, value in opts:
    if option in ["-h", "--help"]:
        print("""  
        usage:%s --url=[value] --order=[value] --help=[value] --depth=[value]
        --delay=[value] --crawl_id=[value]
        """)
    elif option in ['--url', '-u']:
        config["url"] = value
    elif option in ['--order', '-o']:
        config["order"] = value
    elif option in ['--deepth', '-d']:
        config["depth"] = value
    elif option in ['--delay', '-e']:
        config["delay"] = value
    elif option in ['--crawl_id', '-c']:
        config["crawl_id"] = value
#settings的设置
sett = get_project_settings()
sett['DOWNLOAD_DELAY'] = config["delay"]
sett['USER_AGENT'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.13 Safari/537.36'
sett['DEPTH_LIMIT'] = config["depth"]#2
order = config['order']
if order=='DFO':
    pass#系统默认是深度优先
elif order=='BFO':
    sett['DEPTH_PRIORITY'] = 1
    sett['SCHEDULER_DISK_QUEUE'] = 'scrapy.squeue.PickleFifoDiskQueue'
    sett['SCHEDULER_MEMORY_QUEUE'] = 'scrapy.squeue.FifoMemoryQueue'
    print("hhhhhhhhhhhhhh")
date1 = datetime.now().replace(microsecond=0)
print("开始时间："+str(date1))
process = CrawlerProcess(sett)
url = []
url.append(config['url'])
print(url)
process.crawl(MySpider, url_list = url)#['http://news.qq.com.cn/'])
process.start()
date2 = datetime.now().replace(microsecond=0)
print("结束时间："+str(date2))
get_crawl(url,order,date1,date2)

