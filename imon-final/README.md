# iMon

## 大目标：多个网站和javascript支持

### 一、功能

#### 爬虫功能

- 多个目标网站，按照**中目标 **里的要求抓取和分析
- 理解javascript
- 应对目标网站可能出现的反爬虫措施

#### 爬虫配置项

- 目标网站列表，可以动态添加
- 针对各个目标网站，有各自独立的**中目标**里的所有配置
- 针对各个目标网站，配置是否支持javascript

#### 数据分析

- 功能： 对抓取的网页做信息统计，输出结果包含（不限于）

  - 抓取任务执行了多久
  - 一共抓了多少个网页/资源


-   每个网页平均含有几个链接
-   整个网站一共有多少个外链的域名，每个域名有多少次
    - 网页的平均大小
    - 网页 的大小分布

     输出结果可以为数字统计或图表

### 二、环境

- Windows7 64位+python3.6+scrapy+selenium+pymysql+matplotlib+wampserver+firefox+geckodriver

  两个文件夹tencent和datachart

  - tencent用于抓取网站信息并存入数据库，需要在wampserver里面建立一个first数据库，建立page，url，crawl三个数据表，具体结构如下：

    page表：

      ![p0](/imon-final/screenshot/p0.PNG)

  ​	url表：

  ​![u0](/imon-final/screenshot/u0.PNG)

  ​	 crawl表：  	
  ![c0](/imon-final/screenshot/c0.PNG)

- datachart用于统计分析数据库里的内容，需要在first里面添加一个exdomains的数据表

    ![e0](/imon-final/screenshot/e0.PNG)

### 三、主要函数介绍

- 抓取程序

  使用了scrapy框架

  - run.py

    - 功能：主程序

    - ```python
      class MySpider(CrawlSpider):
         name = 'myspider'
         domains = set()
         # 配置_init_函数，传入start_url，爬虫id，是否动态抓取的布尔值以及过滤规则
         def __init__(self,crawl_id=None,dyna=False,moreparams=None,*args,**kwargs)
         #配置start_requests，可以根据self.dyna确定使用动态分析函数还是静态分析函数
         def start_requests(self)
         # 当爬虫退出的时候关闭firefox
         def spider_closed(self, spider)
         # 单网页静态分析函数
         def parse_item(self, response)
         # 动态单网页的分析
         def parse_dynamic(self, response)
      ```

    - ```python
      # 函数用来存储爬虫start_url，配置，开始时间和结束时间
      def get_crawl(url, cid, order, typ, js, date1, date2)
      ```

    - ```python
      def get_cmd():  # 从命令行读取参数
      ```

    - ```python
      def get_settings():  # settings的设置
      ```

  - pipelines.py

    - ```python
      class TencentPipeline(object):
          def __init__(self):# 和本地的newsDB数据库建立连接
          def process_item(self, item, spider)#将item中的内容存入到数据库
      ```

  - items.py

    - ```python
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
      ```

  - settings.py

    - ```python
      ROBOTSTXT_OBEY = True
      ITEM_PIPELINES = {
          'tencent.CustomURLFilter.CustomURLFilter':100,
          'tencent.pipelines.TencentPipeline': 300,
      }
      ```

  - CustomURLFilter.py

    - ```python
      class CustomURLFilter(object): """根据url过滤"""
            def __init__(self):#构造队列
            def request_seen(self,item,spider):#检查是否url在队列中
      ```

- 分析程序

  ```python
  def get_cmd()#从命令行读取参数
  def get_mysql()#连接数据库
  def get_time(cid)#抓取任务执行了多久
  def get_page(cid)#一共抓了多少个网页/资源
  def get_links(cid)#每个网页平均含有几个链接
  def get_domains(cid,page)#整个网站一共有多少个外链的域名，每个域名有多少次,将结果存入到数据库exdomains
  def get_size(cid)#网页的平均大小
  def get_pagebar(cid)#网页的大小分布柱状图
  def get_chart(x,y)# 分组画柱状图
  if __name__ == "__main__"#主函数
  ```

  ​

### 四、实验结果

##### 网站的静态分析

- 打开命令行窗口：

  ```python
  python myspider.py --url=http://news.qq.com/ --order=DFO --depth=1 --delay=1 --type=.htm --crawl_id=1
  ```

  爬取http://news.qq.com/，order：深度优先，depth：遍历一层，delay：下载延迟1秒，type：允许过滤含有.htm的网页，crawl_id：爬虫id为1，默认为静态分析


- 完成之后

  - 数据表page 

    ![p1](/imon-final/screenshot/p1.PNG)

  - 数据表url

     ![u1](/imon-final/screenshot/u1.PNG)

  - 数据表crawl

    ![c1](/imon-final/screenshot/c1.PNG)


- datachart

  - 命令行输入：

    ```python
    python analysis.py --crawl_id=1
    ```

  - 窗口输出：

      ![cc1](/imon-final/screenshot/cc1.PNG)

  - 数据表exdomains

      ![e1](/imon-final/screenshot/e1.PNG)

    ...

      ![e11](/imon-final/screenshot/e11.PNG)

  - 柱状图

     ![ccc1](/imon-final/screenshot/ccc1.PNG)


##### 网站的动态分析

- 打开命令行窗口：

```python
python myspider.py --url=http://news.qq.com/ --order=DFO --depth=1 --delay=1 --type=.htm --crawl_id=2 --js=true
```

爬取http://news.qq.com/，深度优先，遍历一层，下载延迟1秒，允许过滤含有.htm的网页，爬虫id为2，支持JavaScript

- 完成之后

  - page：

    ![p2](/imon-final/screenshot/p2.PNG)

  - url：

      ![u2](/imon-final/screenshot/u2.PNG)

  - crawl：

      ![c2](/imon-final/screenshot/c2.PNG)



- datachart

  - 命令行输入：

    ```python
    python analysis.py --crawl_id=2
    ```

  - 数据表exdomains：

      ![e2](/imon-final/screenshot/e2.PNG)

    ...

     ![e22](/imon-final/screenshot/e22.PNG)

  - 窗口输出：

      ![cc2](/imon-final/screenshot/cc2.PNG)

  - 柱状图：

    ![ccc2](/imon-final/screenshot/ccc2.PNG)

以上网页都以TXT形式存储到D:\testFile\html文件夹下面

 ![t0](/imon-final/screenshot/t0.PNG)

### 五、实验结论

​	在采集了大量数据分析后，静态分析网站仅仅只爬取网页源代码里面的内容，动态加载的内容并没有获取到，动态分析网站则是用selenium模拟浏览器访问网站，实时获取到动态加载内容的源代码，相比于静态分析所抓取的网页链接以及网页大小，动态分析要多一些，但是动态爬取效率要更低，耗时长。

### 六、对于特定动态网站的采集

- 对于新浪财经的[沪深股市](http://finance.sina.com.cn/data/#stock?qq-pf-to=pcqq.group)的代码、名称、最新价、涨跌额、涨跌幅、买入、卖出、昨收、今开、最高、最低、成交量（手）、成交额（万）进行采集，发现在点击"<u>下一页</u>"的时候，url并没有发生变化，于是直接用selenium的webdriver模拟点击下一页的操作

```python
new_site = self.browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[4]/div[2]/span[3]')
new_site.click()
```

即可实现整个栏目的遍历（找到最大页码，在循环中逐页访问）

```python
total = self.browser.find_element_by_xpath
('/html/body/div[3]/div[3]/div[4]/div[2]/span[5]/span[2]')
total = total.text#总页数
for i in range(int(total)):
...
```

![s0](/imon-final/screenshot/s0.PNG)

- 对[斗鱼直播平台](https://www.douyu.com/directory/game/wzry)的标题、直播人、栏目、观看人数进行采集，同样在点击"下一页"的时候，url没变，但打开调试工具的时候，浏览器发送了一个Request URL：https://www.douyu.com/directory/game/wzry?**page=2**&isAjax=1其中page=2代表了当前页数，于是直接返回上述Request URL，page动态传入

  ```python
  self.page +=1
  if self.page<=self.maxpage:
  	yield scrapy.Request('https://www.douyu.com/directory/game/wzry?page=%d&isAjax=1' % self.page)
  ```

  每调用分析函数一次self.page就增加1，但不大于在首页中找到的最大页码self.maxpage。	

  于是对网页的分析分为两种，一个是首页，另一个是返回的数据表单，通过if-else分隔，区别在于xpath的写法不一样。![dy-1](/imon-final/screenshot/dy-1.PNG)

  ​ ![dy-0](/imon-final/screenshot/dy-0.PNG)

### 七、反爬措施

- 基于headers

  ```python
  sett['USER_AGENT'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.13 Safari/537.36'
  ```

- 基于用户行为，访问频率

  ```python
  sett['DOWNLOAD_DELAY'] = config["delay"]
  ROBOTSTXT_OBEY = False
  ```

- 基于动态页面

  ```python
  # 动态单网页的分析
  def parse_dynamic(self, response)
  ```

### 八、断点续爬

在myspider.py文件里加入settings的JOBDIR参数：

```python
sett['JOBDIR'] = config["jobdir"]
```

就会在运行爬虫后，对应的文件夹下面产生相应的目录存放队列，在命令行输入的时候加上--jobdir=xxx，按下Ctrl+c就可停止，再次启动就是跟上次命令一样。下面有两个例子

 ![dd-4](/imon-final/screenshot/dd-4.PNG)

断点续爬直接输入上一次的命令：

 ![dd-5](/imon-final/screenshot/dd-5.PNG)

数据库查看第一次爬取的起始url：

![dd-55](/imon-final/screenshot/dd-55.PNG)

续爬后的起始url： ![dd-44](/imon-final/screenshot/dd-44.PNG)

百度贴吧的例子：

 ![dd-6](/imon-final/screenshot/dd-6.PNG)

 ![dd-66](/imon-final/screenshot/dd-66.PNG)



![dd-666](/imon-final/screenshot/dd-666.PNG)



