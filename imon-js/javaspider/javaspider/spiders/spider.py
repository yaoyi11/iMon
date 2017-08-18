# encoding: utf-8
import time

import scrapy
from scrapy.spider import Spider
from selenium import webdriver
from bs4 import BeautifulSoup  # 使用bs4中beautifulsoup解析
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from javaspider.items import JavaspiderItem
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class LiCaiSpider(Spider):
    name = "LiCai"
    allowed_domains = ["finance.sina.com.cn"]
    start_urls = [
        "http://finance.sina.com.cn/data/#stock?qq-pf-to=pcqq.group"
#        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def __init__(self):
        self.browser = webdriver.Firefox() #使用前请安装对应的webdriver
        # 设定页面加载限制时间

    # def __del__(self):
    #     self.browser.close()

    def parse(self, response):
        item = JavaspiderItem()
        #start browser
        self.browser.set_page_load_timeout(10)
        self.browser.set_script_timeout(10)  # 这两种设置都进行才有效
        self.browser.maximize_window()
        try:
            self.browser.get(response.request.url)
            time.sleep(4)
            self.browser.find_element_by_xpath('//*[@id="numberDiv_0"]/a[3]').click()
            time.sleep(3)  # 休眠两秒
        except TimeoutException:
            print('time out after 30 seconds when loading page')
            self.browser.execute_script('window.stop()') #当页面加载时间超过设定时间
        total = self.browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[4]/div[2]/span[5]/span[2]')
        total = total.text
        for i in range(int(total)):
            try:
                sreach_window = self.browser.current_window_handle
                # wait = WebDriverWait(self.browser, 10)
                # element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[4]/div[1]/table/tbody/tr[80]')))

                con = []
                for it in self.browser.find_elements_by_xpath('/html/body//table[@id="block_1"]/tbody/tr'):
                    con.append(it.text)
                #con = con[2:-2]
                for i in range(len(con)):
                    cc = con[i].split(' ')
                    item['daima'] = cc[0]  # 代码
                    item['name'] = cc[1]  # 名称
                    item['latest_price'] = cc[2]  # 最新价
                    item['zhangdie'] = cc[3]  # 涨跌额
                    item['zhangdiefu'] = cc[4]  # 涨跌幅
                    item['buy_in'] = cc[5]  # 买入
                    item['sell_out'] = cc[6]  # 卖出
                    item['yesterday'] = cc[7]  # 昨收
                    item['today'] = cc[8]  # 今开
                    item['high'] = cc[9]  # 最高
                    item['low'] = cc[10]  # 最低
                    c1 = cc[11].replace(',','')
                    item['dillcount'] = int(c1)  # 成交量（手）
                    c2 = cc[12].replace(',','')
                    item['dillmon'] = c2  # 成交额（万）
                    yield item
            except Exception as e:
                print(e)
            new_site = self.browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[4]/div[2]/span[3]')
            new_site.click()
            time.sleep(6)