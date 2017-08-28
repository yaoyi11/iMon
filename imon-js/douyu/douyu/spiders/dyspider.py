# encoding: utf-8
import time

import scrapy
from scrapy.spider import Spider
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from douyu.items import DouyuItem
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class LiCaiSpider(Spider):
    name = "douyu"
    page = 1#首页
    maxpage = 0#最后一页
    allowed_domains = ["www.douyu.com"]
    start_urls = [
        "https://www.douyu.com/directory/game/wzry"
    ]

    def __init__(self):
        self.browser = webdriver.Firefox() #使用前请安装对应的webdriver

    def parse(self, response):
        item = DouyuItem()
        #start browser
        self.browser.set_page_load_timeout(10)
        self.browser.set_script_timeout(10)  # 这两种设置都进行才有效
        self.browser.maximize_window()
        try:
            self.browser.get(response.request.url)
            time.sleep(4)
        except TimeoutException:
            print('time out after 30 seconds when loading page')
            self.browser.execute_script('window.stop()') #当页面加载时间超过设定时间关闭窗口
        content = []
        try:
            str = 'page'
            #第二页及以后的页面的分析
            if str in response.request.url:
                for i in self.browser.find_elements_by_xpath('/html/body/li'):
                    content.append(i.text)
                print("----------------page----------")
                for j in content:
                    con = j.split('\n')
                    item['title'] = con[0]#标题
                    item['lanmu'] = con[1]#分类
                    cc = con[2].split(' ')
                    item['user'] = cc[0]#主播
                    item['followers'] = cc[1]#观看人数
                    yield item
            #首页的分析
            else:
                maxpage = self.browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div/div/div[4]/a[10]').text
                self.maxpage = int(maxpage)
                for i in self.browser.find_elements_by_xpath('/html/body/div[2]/div[3]/div[1]/div/div/div[3]/ul/li'):
                    content.append(i.text)
                for j in content:
                    con = j.split('\n')
                    item['title'] = con[0]
                    item['lanmu'] = con[1]
                    item['user'] = con[2]
                    item['followers'] = con[3]
                    yield item
        except:
            pass
        #请求下一页
        self.page +=1
        #若是超过最大页码就停止
        if self.page<=self.maxpage:
            yield scrapy.Request('https://www.douyu.com/directory/game/wzry?page=%d&isAjax=1' % self.page)
        else:
            self.browser.quit()
            print("爬虫结束！")