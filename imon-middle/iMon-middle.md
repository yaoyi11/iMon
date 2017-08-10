# iMon

## 中目标：单个网站静态分析

### 一、功能

#### 爬虫功能

- 对整个目标网站或目标网站的一个栏目进行采集。采集内容不超出该网站或栏目
- 正确处理网页编码。
- 可以过滤特定的资源类型。如只抓取htm/html/txt等文本内容，不采集图片，视频等信息
- 可以断点恢复。遇到采集过程中断，可以在恢复正常后接着采集，而不是从头再来。
- 友好的信息采集。使用适当的延迟/间隔访问目标网站，不给目标网站造成严重的压力。

#### 爬虫配置项

- 目标url
- 选项：深度优先或广度优先
- 配置项：不采集的资源类型列表。根据文件后缀或是HTTP协议标明的资源类型。



#### 数据分析

- 单网页分析，包括不限于
  - 大小
  - 编码
  - 标题
  - 抓取时间
  - 所有的链接地址的域名
- 统计分析
  - 网页数量
  - 网页大小分布
  - 所有链接地址的域名统计


### 二、目标网站

- 腾讯新闻

### 三、环境

- Windows7 64位+python3.6+pycharm-community-2017.1.5+wampserver

  pycharm导入两个文件夹tencent和datachart

  - tencent用于抓取网站信息并存入数据库，需要在wampserver里面建立一个first数据库，建立page和url两个数据表，具体结构如下：

  ![3](C:\Users\yy\Desktop\diary\png\3.PNG)

  ![4](file:///C:/Users/yy/Desktop/diary/png/4.PNG?lastModify=1502254827)

  - datachart用于统计分析数据库里的内容，需要在first里面添加一个exdomains的数据表

  ![5](C:\Users\yy\Desktop\diary\png\5.PNG)

### 四、实验结果

- tencent

  - 窗口：

    ```html
    数据成功插入！
    2017-08-10 09:51:40 [scrapy.core.scraper] DEBUG: Scraped from <200 http://news.qq.com/a/20170809/001748.htm>
    {'charset': 'gb2312',
     'date': '2017-08-10 09:51:39',
     'domain': {'dz.jjckb.cn',
                'ehsb.hsw.cn',
                'gongyi.qq.com',
                'history.news.qq.com',
                'hr.tencent.com',
                'iwan.qq.com',
                'kaifu.qq.com',
                'm.news.cctv.com',
                'mil.huanqiu.com',
                'mil.qq.com',
                'military.cnr.cn',
                'news.haiwainet.cn',
                'news.qq.com',
                'news.xinhuanet.com',
                'newspaper.jfdaily.com',
                'open.qq.com',
                'paper.people.com.cn',
                'service.qq.com',
                'support.qq.com',
                't.qq.com',
                'v.qq.com',
                'view.news.qq.com',
                'view.qq.com',
                'weather.news.qq.com',
                'world.huanqiu.com',
                'www.chinanews.com',
                'www.fawan.com',
                'www.fmprc.gov.cn',
                'www.qq.com',
                'www.sogou.com',
                'www.tencent.com',
                'www.tencentmind.com',
                'www.xinhuanet.com',
                'xhpfm.mobile.zhongguowangshi.com',
                'xhpfmapi.zhongguowangshi.com'},
     'size': 38283,
     'title': ['中国地震局：九寨沟震区近日仍存在6级左右余震可能'],
     'url': 'http://news.qq.com/a/20170809/001748.htm'}
    ```

    诸如此类

  - 数据表page

     ![6](C:\Users\yy\Desktop\diary\png\6.PNG)

    ...

    ![7](C:\Users\yy\Desktop\diary\png\7.PNG)

  - 数据表url

     ![8](C:\Users\yy\Desktop\diary\png\8.PNG)


​		...

​		 ![9](C:\Users\yy\Desktop\diary\png\9.PNG)


- datachart

  - 窗口

    ```
    已存入数据库的网页数量是：128
    已将结果存入表exdomains中！
    ```

  - 数据表exdomains

     ![10](C:\Users\yy\Desktop\diary\png\10.PNG)

    ...

     ![11](C:\Users\yy\Desktop\diary\png\11.PNG)

  - 柱状图

     ![12](C:\Users\yy\Desktop\diary\png\12.PNG)




