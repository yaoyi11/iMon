# -*- coding: utf-8 -*-
import codecs
import os
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from scrapy import Request, crawler
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.utils.project import get_project_settings
import pymysql

from tencent.items import TencentItem
import getopt
import sys
import time
import re
from bs4 import BeautifulSoup

class MySpider(CrawlSpider):
    name = 'myspider'
    #links = set()
    domains = set()
    #配置_init_函数，传入allow过滤规则，start_url
    def __init__(self, dyna = None, moreparams = None, *args, **kwargs):
        self.dyna = dyna
        if dyna==1:
            self.start_urls = kwargs.pop('url_list', [])  # 开始的url
            domain = self.start_urls[0].strip().split('/')[2]
            # print(self.start_urls[0].strip().split('/'))
            self.allowd_domains = []
            self.allowd_domains.append(domain)  # 域名限制
            super(MySpider, self).__init__(*args, **kwargs)  # 这里是关键
            MySpider.rules = (Rule(LinkExtractor(allow=moreparams), callback="parse_item", follow=True),)
            self.moreparams = moreparams
            super(MySpider, self)._compile_rules()  # 重写rule规则
        if dyna ==2:
            self.browser = webdriver.Firefox()  # 使用前请安装对应的webdriver
            self.start_urls = kwargs.pop('url_list', [])  # 开始的url
            domain = self.start_urls[0].strip().split('/')[2]
            self.allowd_domains = []
            self.allowd_domains.append(domain)  # 域名限制
            super(MySpider, self).__init__(*args, **kwargs)  # 这里是关键

    def start_requests(self):
        if self.dyna == 2:
            for url in self.start_urls:
                yield scrapy.Request(url,callback=self.parse_dynamic)
        else:
            for url in self.start_urls:
                yield scrapy.Request(url,callback=self.parse_item)

    #单网页分析函数
    def parse_item(self, response):
        global domains
        qqnews = TencentItem()
        setting = self.settings
        depth = int(setting['DEPTH_LIMIT'])#设置的爬取深度
        #self.domains.add(self.allowd_domains[0])
        try:

            qqnews['url'] = response.url#url地址
            # self.links.add(response.url)
            qqnews['title'] = response.xpath('//html/head/title/text()').extract()#标题
            #时间中的秒数为整数
            qqnews['date'] = str(datetime.now().replace(microsecond=0))#抓取时间
            charset = response.encoding
            qqnews['charset'] = charset#网页编码
            qqnews['size'] = len(response.body)#网页大小
            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%Y%m%d-%H%M%S")  # 时间用作标题
            #将网页内容写入到txt文件中
            filename = 'D:\\testFile\\html\\' + otherStyleTime + '.txt'
            fp = codecs.open(filename, "w+", charset)  # 保存在html文件夹下
            content = response.body.decode(charset,'ignore')
            fp.write(content)
            fp.close()
            qqnews['filepath'] = filename#文件存放的路径
            #找到网页里所有链接地址
            for site in response.xpath("//a/@href").re(r'^http[s]{0,1}:[a-zA-Z0-9\/\?\=].*'):
                #if site not in self.links:#新链接
                try:
                    n = site.strip().split('/')[2]#提取域名
                    self.domains.add(n)
                except:
                    pass
            qqnews['domain'] = self.domains
            yield qqnews
        except:
            pass

        meta = response.meta  # 方便检测实时爬取的深度
        if meta['depth']<depth:#在爬取深度范围内
            for url in response.selector.xpath("//a/@href").re(r'^http[s]{0,1}://%s/[a-zA-Z0-9\/\?\=].*' % self.allowd_domains[0]):
                #print(url)
                yield scrapy.Request(url, callback=self.parse_item )#返回request
        else:
            process.stop()#超出范围就停止

    def parse_dynamic(self, response):
        global domains
        qqnews = TencentItem()
        setting = self.settings
        depth = int(setting['DEPTH_LIMIT'])  # 设置的爬取深度
        # start browser
        self.browser.set_page_load_timeout(10)
        self.browser.set_script_timeout(10)  # 这两种设置都进行才有效
        self.browser.maximize_window()
        self.browser.get(response.request.url)
        time.sleep(4)
        try:
            yuan = self.browser.page_source
            qqnews['url'] = response.request.url#url地址
            qqnews['title'] = self.browser.title#self.browser.find_element_by_xpath('//html/head/title/text()').extract()#标题
            #时间中的秒数为整数
            qqnews['date'] = str(datetime.now().replace(microsecond=0))#抓取时间
            charset = response.encoding
            qqnews['charset'] = charset#网页编码
            qqnews['size'] = len(yuan)#网页大小
            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%Y%m%d-%H%M%S")  # 时间用作标题
            #将网页内容写入到txt文件中
            filename = 'D:\\testFile\\html\\' + otherStyleTime + '.txt'
            fp = codecs.open(filename, "w+", charset)  # 保存在html文件夹下
                #content = yuan.decode(charset,'ignore')
            fp.write(yuan)
            fp.close()
            qqnews['filepath'] = filename#文件存放的路径
            #找到网页里所有链接地址
            links = []
            for link in self.browser.find_elements_by_tag_name("a"):
                links.append(link.get_attribute("href"))
            for site in links:
                try:
                    n = site.strip().split('/')[2]#提取域名
                    self.domains.add(n)
                except:
                    pass
            qqnews['domain'] = self.domains
            yield qqnews
        except:
            pass

        meta = response.meta  # 方便检测实时爬取的深度
        if meta['depth'] < depth:  # 在爬取深度范围内
            for url in links:
                if url:
                    print('^http[s]{0,1}://%s/[a-zA-Z0-9\/\?\=].*' % self.allowd_domains[0])
                    if re.search('^http[s]{0,1}://news.qq.com/[a-zA-Z0-9\/\?\=].*',url):
                        print(url)
                        yield scrapy.Request(url, callback=self.parse_dynamic)  # 返回request
        else:
            process.stop()  # 超出范围就停止
        time.sleep(3)  # 休眠两秒

#函数用来存储爬虫start_url，配置，开始时间和结束时间
def get_crawl(url, order, skip, date1, date2):
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
    site = url[0]
    skip = skip
    order = order
    start_time = date1
    end_time = date2
    sql = "INSERT INTO crawl(url,`order`,skip,start_time,end_time) VALUES ('%s', '%s', '%s',\'%s\', \'%s\')" % (site, order, skip, start_time, end_time)
    cursor.execute(sql)

    conn.commit()
    print("success！！")

def get_cmd():#从命令行读取参数
    #初始化
    config = {
        "url": "http://news.qq.com/",
        "order": "DFO",
        "depth": "1",
        "delay": "2",
        "skip": ".htm",
        "crawl_id": "1"
    }
    opts, args = getopt.getopt(sys.argv[1:], 'u:o:d:e:s:c:h',['url=','order=','depth=','delay=','skip=','crawl_id=','help'])
    # 参数的解析过程,长参数为--，短参数为-
    for option, value in opts:
        if option in ["-h", "--help"]:
            print("""  
            usage:%s --url=[value] --order=[value] --help=[value] --depth=[value]
            --delay=[value] --skip=[value] --crawl_id=[value]
            """)
        elif option in ['--url', '-u']:
            config["url"] = value
        elif option in ['--order', '-o']:
            config["order"] = value
        elif option in ['--deepth', '-d']:
            config["depth"] = value
        elif option in ['--delay', '-e']:
            config["delay"] = value
        elif option in ['--skip', '-s']:
            config["skip"] = value
        elif option in ['--crawl_id', '-c']:
            config["crawl_id"] = value
    return config

def get_settings():# settings的设置
    sett = get_project_settings()
    config = get_cmd()
    sett['DOWNLOAD_DELAY'] = config["delay"]
    sett['USER_AGENT'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.13 Safari/537.36'
    sett['DEPTH_LIMIT'] = config["depth"]  #
    order = config['order']
    if order == 'DFO':
        pass  # 系统默认是深度优先
    elif order == 'BFO':
        sett['DEPTH_PRIORITY'] = 1
        sett['SCHEDULER_DISK_QUEUE'] = 'scrapy.squeue.PickleFifoDiskQueue'
        sett['SCHEDULER_MEMORY_QUEUE'] = 'scrapy.squeue.FifoMemoryQueue'
        print("已设置成广度优先...")
    return sett

config = get_cmd()
sett = get_settings()
order = config['order']
skip = config['skip']
date1 = datetime.now().replace(microsecond=0)
print("开始时间：" + str(date1))
process = CrawlerProcess(sett)
url = []
url.append(config['url'])
process.crawl(MySpider, dyna = 2, moreparams=skip, url_list=url)  # ['http://news.qq.com.cn/'])
process.start()
date2 = datetime.now().replace(microsecond=0)
print("结束时间："+str(date2))
get_crawl(url,order,skip,date1,date2)

