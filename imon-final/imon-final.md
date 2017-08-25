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

    ![p0](diary\final\p0.PNG)

     url表：

    ![u0](diary\final\u0.PNG)

     crawl表：

    ![c0](diary\final\c0.PNG)


- datachart用于统计分析数据库里的内容，需要在first里面添加一个exdomains的数据表

    ![e0](diary\final\e0.PNG)

### 三、主要函数介绍

- 抓取程序
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

  爬取http://news.qq.com/，深度优先，遍历一层，下载延迟1秒，允许过滤含有.htm的网页，爬虫id为1，静态分析


- 完成之后

  - 数据表page 

    ![p1](diary\final\p1.PNG)

  - 数据表url

      ![u1](diary\final\u1.PNG)

  - 数据表crawl

    ![c1](diary\final\c1.PNG)


- datachart

  - 命令行输入：

    ```python
    python analysis.py --crawl_id=1
    ```

  - 窗口输出：

      ![cc1](diary\新建文件夹\cc1.PNG)

  - 数据表exdomains

       ![e1](diary\新建文件夹\e1.PNG)

    ...

      ![e11](diary\新建文件夹\e11.PNG)

  - 柱状图 ![ccc1](diary\新建文件夹\ccc1.PNG)


##### 网站的动态分析

- 打开命令行窗口：

```python
python run.py --url=http://news.qq.com/ --order=DFO --depth=1 --delay=1 --type=.htm --crawl_id=2 --js=true
```

爬取http://news.qq.com/，深度优先，遍历一层，下载延迟1秒，允许过滤含有.htm的网页，爬虫id为2，动态分析

- 完成之后

  - page：

    ![p2](diary\新建文件夹\p2.PNG)

  - url：

      ![u2](diary\新建文件夹\u2.PNG)

  - crawl：  ![c2](diary\新建文件夹\c2.PNG)



- datachart

  - 命令行输入：

    ```python
    python test3.py --crawl_id=2
    ```

  - 数据表exdomains：

      ![e2](diary\新建文件夹\e2.PNG)

    ...

     ![e22](diary\新建文件夹\e22.PNG)

  - 窗口输出：

      ![cc2](diary\新建文件夹\cc2.PNG)

  - 柱状图：

    ![ccc2](diary\新建文件夹\ccc2.PNG)

以上网页都以TXT形式存储到D:\testFile\html文件夹下面

 ![t0](diary\新建文件夹\t0.PNG)

### 五、实验结论

​	在采集了大量数据分析后，动态分析网站相比静态分析所抓取的网页链接以及网页大小，前者要多一些，但是动态爬取效率要更低，耗时长。

### 六、对于特定动态网站的采集

对于新浪财经的[沪深股市](http://finance.sina.com.cn/data/#stock?qq-pf-to=pcqq.group)进行采集，发现在点击"<u>下一页</u>"的时候，url并没有发生变化，于是直接用selenium的webdriver模拟点击下一页的操作

```python
new_site = self.browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[4]/div[2]/span[3]')
new_site.click()
```

即可实现整个栏目的遍历

![s0](diary\新建文件夹\s0.PNG)