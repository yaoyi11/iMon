# -*- coding: utf-8 -*-
import codecs
import os
from datetime import datetime

from pydispatch import dispatcher
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
from scrapy import signals


class MySpider(CrawlSpider):
    name = 'myspider'
    domains = set()

    # 配置_init_函数，传入start_url，爬虫id，是否动态抓取的布尔值以及过滤规则
    def __init__(self, crawl_id=None, dyna=False, moreparams=None, *args, **kwargs):
        self.crwal_id = crawl_id#爬虫id
        self.dyna = dyna#是否动态抓取
        self.moreparams = moreparams#过滤条件
        if not self.dyna:
            self.start_urls = kwargs.pop('url_list', [])  # 开始的url
            domain = self.start_urls[0].strip().split('/')[2]
            self.allowd_domains = []
            self.allowd_domains.append(domain)  # 域名限制
            super(MySpider, self).__init__(*args, **kwargs)  # 这里是关键
        else:
            self.browser = webdriver.Firefox()  # 使用前请安装对应的webdriver
            self.start_urls = kwargs.pop('url_list', [])  # 开始的url
            domain = self.start_urls[0].strip().split('/')[2]
            self.allowd_domains = []
            self.allowd_domains.append(domain)  # 域名限制
            super(MySpider, self).__init__(*args, **kwargs)  # 这里是关键
            dispatcher.connect(self.spider_closed, signals.spider_closed)

    #配置start_requests，可以根据self.dyna确定使用动态分析函数还是静态分析函数
    def start_requests(self):
        #动态分析
        if self.dyna:
            for url in self.start_urls:
                yield scrapy.Request(url, callback=self.parse_dynamic)
        else:#静态分析
            for url in self.start_urls:
                yield scrapy.Request(url, callback=self.parse_item)

    # 当爬虫退出的时候关闭firefox
    def spider_closed(self, spider):
        print("爬虫结束！")
        self.browser.quit()

    # 单网页静态分析函数
    def parse_item(self, response):
        global domains
        qqnews = TencentItem()
        setting = self.settings
        depth = int(setting['DEPTH_LIMIT'])  # 设置的爬取深度
        try:
            qqnews['crawl_id'] = self.crwal_id
            qqnews['url'] = response.url  # url地址
            qqnews['title'] = response.xpath('//html/head/title/text()').extract()  # 标题
            # 时间中的秒数为整数
            qqnews['date'] = str(datetime.now().replace(microsecond=0))  # 抓取时间
            charset = response.encoding
            qqnews['charset'] = charset  # 网页编码
            qqnews['size'] = len(response.body)  # 网页大小
            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%Y%m%d-%H%M%S")  # 时间用作标题
            # 将网页内容写入到txt文件中
            filename = 'D:\\testFile\\html\\' + otherStyleTime + '.txt'
            fp = codecs.open(filename, "w+", charset)  # 保存在html文件夹下
            content = response.body.decode(charset, 'ignore')
            fp.write(content)
            fp.close()
            qqnews['filepath'] = filename  # 文件存放的路径
            # 找到网页里所有链接地址
            trlinks = set()
            for site in response.xpath("//a/@href").re(r'^http[s]{0,1}:[a-zA-Z0-9\/\?\=].*'):
                try:
                    n = site.strip().split('/')[2]  # 提取域名
                    self.domains.add(n)
                    trlinks.add(site)
                except:
                    pass
            qqnews['domain'] = self.domains#域名
            qqnews['count'] = len(trlinks)#含有链接数
            yield qqnews
            self.domains.clear()
        except:
            pass

        meta = response.meta  # 方便检测实时爬取的深度
        if meta['depth'] < depth:  # 在爬取深度范围内
            for url in response.selector.xpath("//a/@href").re(
                            r'^http[s]{0,1}://%s/[a-zA-Z0-9\/\?\=].*' % self.allowd_domains[0]):
                if self.moreparams in url:
                    yield scrapy.Request(url, callback=self.parse_item)  # 返回request

    # 动态单网页的分析
    def parse_dynamic(self, response):
        global domains
        qqnews = TencentItem()
        setting = self.settings
        depth = int(setting['DEPTH_LIMIT'])  # 设置的爬取深度
        # start browser
        # self.browser.set_page_load_timeout(20)
        # self.browser.set_script_timeout(20)  # 这两种设置都进行才有效
        try:
            # self.browser.maximize_window()
            self.browser.get(response.request.url)

            qqnews['crawl_id'] = self.crwal_id
            yuan = self.browser.page_source  # 解析后的网页源代码
            qqnews['url'] = response.request.url  # url地址
            qqnews['title'] = self.browser.title  # 标题
            # 时间中的秒数为整数
            qqnews['date'] = str(datetime.now().replace(microsecond=0))  # 抓取时间
            charset = response.encoding
            qqnews['charset'] = charset  # 网页编码
            qqnews['size'] = len(yuan)  # 网页大小
            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%Y%m%d-%H%M%S")  # 时间用作标题
            # 将网页内容写入到txt文件中
            filename = 'D:\\testFile\\html\\' + otherStyleTime + '.txt'
            fp = codecs.open(filename, "w+", charset)  # 保存在html文件夹下
            # content = yuan.decode(charset,'ignore')
            fp.write(yuan)
            fp.close()
            qqnews['filepath'] = filename  # 文件存放的路径
            # 找到网页里所有链接地址
            trlinks = set()
            # for link in self.browser.find_elements_by_tag_name("a"):
            #     trlinks.add(link.get_attribute("href"))
            for link in BeautifulSoup(yuan, 'lxml').find_all(name='a',attrs={"href":re.compile(r'^http[s]{0,1}:')}):
                #print(link.get('href'))
                trlinks.add(link.get('href'))
            for site in trlinks:
                try:
                    n = site.strip().split('/')[2]  # 提取域名
                    self.domains.add(n)
                except:
                    pass
            qqnews['domain'] = self.domains#全部域名
            qqnews['count'] = len(trlinks)#所有链接数目
            yield qqnews
            self.domains.clear()
        except ConnectionRefusedError:
            self.browser.quit()
        except ConnectionResetError:
            self.browser.quit()
        else:
            meta = response.meta  # 方便检测实时爬取的深度
            if meta['depth'] < depth:  # 在爬取深度范围内
                for url in trlinks:
                    if url:
                        if self.allowd_domains[0] in url:
                            if self.moreparams in url:
                                yield scrapy.Request(url, callback=self.parse_dynamic)  # 返回request


# 函数用来存储爬虫start_url，配置，开始时间和结束时间
def get_crawl(url, cid, order, typ, js, date1, date2):
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
    if js:
        java = 1#动态
    else:
        java = 0#静态
    start_time = date1
    end_time = date2
    sql = "INSERT INTO crawl(url,cid,`order`,allowtype,javascript,start_time,end_time) VALUES ('%s', '%s','%s', '%s', '%s',\'%s\', \'%s\')" % (
    site, cid, order, typ, java, start_time, end_time)
    cursor.execute(sql)

    conn.commit()
    print("success！！")


def get_cmd():  # 从命令行读取参数
    # 初始化默认配置
    config = {
        "url": "http://news.sogou.com/",
        "order": "DFO",
        "depth": "2",
        "delay": "2",
        "type": ".",
        "crawl_id": "1",
        "js": False,
        "jobdir":""
    }
    opts, args = getopt.getopt(sys.argv[1:], 'hu:o:d:e:t:c:j:r:',
                               ['help', 'url=', 'order=', 'depth=', 'delay=', 'type=', 'crawl_id=', 'js=','jobdir='])
    # 参数的解析过程,长参数为--，短参数为-
    for option, value in opts:
        if option in ["-h", "--help"]:
            print("""  
            usage:%s --url=[start_url] --order=[BFO/DFO] --depth=[depth_limit]
            --delay=[delaytime] --type=[value] --crawl_id=[number] --js=[True/False] --jobdir=[value]
            """)
        elif option in ['--url', '-u']:
            config["url"] = value
        elif option in ['--order', '-o']:
            config["order"] = value
        elif option in ['--deepth', '-d']:
            config["depth"] = value
        elif option in ['--delay', '-e']:
            config["delay"] = value
        elif option in ['--type', '-t']:
            config["type"] = value
        elif option in ['--crawl_id', '-c']:
            config["crawl_id"] = value
        elif option in ['--js', '-j']:
            config["js"] = value
        elif option in ['--jobdir', '-r']:
            config["jobdir"] = value
    return config


def get_settings():  # settings的设置
    sett = get_project_settings()
    config = get_cmd()
    sett['DOWNLOAD_DELAY'] = config["delay"]#下载延迟
    sett['USER_AGENT'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.13 Safari/537.36'
    sett['DEPTH_LIMIT'] = config["depth"]  #深度
    sett['JOBDIR'] = config["jobdir"]#断点重连的队列
    order = config['order']
    if order == 'DFO':
        pass  # 系统默认是深度优先
    elif order == 'BFO':
        sett['DEPTH_PRIORITY'] = 1
        sett['SCHEDULER_DISK_QUEUE'] = 'scrapy.squeue.PickleFifoDiskQueue'
        sett['SCHEDULER_MEMORY_QUEUE'] = 'scrapy.squeue.FifoMemoryQueue'
        print("已设置成广度优先...")
    return sett


config = get_cmd()#命令行参数
sett = get_settings()#配置
order = config['order']#深度优先/广度优先
typ = config['type']#过滤类型
js = config['js']#是否动态
cid = config['crawl_id']#爬虫id
date1 = datetime.now().replace(microsecond=0)#开始时间
print("开始时间：" + str(date1))
process = CrawlerProcess(sett)
url = []#start_url
url.append(config['url'])
process.crawl(MySpider, crawl_id=cid, dyna=js, moreparams=typ, url_list=url)  # ['http://news.qq.com/'])
process.start()#开始
date2 = datetime.now().replace(microsecond=0)#结束时间
print("结束时间：" + str(date2))
get_crawl(url, cid, order, typ, js, date1, date2)#存到数据库
