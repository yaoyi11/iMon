# python
## 小目标：单个网页静态分析

### 一、功能

- 对目标网站的一个特定页面进行采集。
- 静态分析，保存分析结果
  - 获取网页的大小
  - 获取网页的标题或特定内容
  - 获取网页里所有的链接地址
- 把采集的结果和分析结果保存在mysql。

### 二、配置项

- 目标url:'http://baike.baidu.com/item/Python

### 三、环境及软件

- Windows7 64位+python3.6+pycharm-community-2017.1.5+wampserver

### 四、安装步骤

- 安装python3.6.2
  - 官网下载python3.6.2的安装包，然后直接按提示操作
    - 检验：在cmd窗口输入python出来版本信息即可
- 安装pycharm-community-2017.1.5
  - 同样在官网下载，直接安装
- 安装BeautifulSoup
  - 去官网下载解压，解压后移到python所在目录下，在cmd窗口下进入到beautifulsoup的目录，执行
    - python setup.py build
    - python setup.py install
    - 在pycharm中导入这个包（ps：在pycharm中可直接下载bs4）
- 安装数据库wampserver
  - 选择Windows7 64位下载即可
  - 可能的出错
    - 丢失msvcr110.dll
    - 修复：在https://www.microsoft.com/zh-CN/download/details.aspx?id=30679下载了x64、x86两种Visual C++
  - 配置：建立一个名字为first的数据库，再建立两个数据表test、url
    - test表中包含两个字段，title，size，类型均为varchar
    - url表中包含两个字段，id，link，类型均为varchar

### 五、结果显示

窗口下的显示：

- file:Python_百度百科.txt
- ALL Down
- 网页标题是：Python_百度百科
- 网页大小是：168976b
- 链接准备存入数据库...
- 数据成功插入！

D盘出现testFile文件夹，文件夹里有Python_百度百科.txt，在数据库first中显示存储结果。

test数据表：

| title       | size   |
| ----------- | ------ |
| Python_百度百科 | 168976 |

url数据表：

| id   | link                                     |
| ---- | ---------------------------------------- |
| 1    | https://bkssl.bdimg.com/static/wiki-lemma/widget/tools/label/label_ca156c6.css |
| 2    | https://bkssl.bdimg.com/static/wiki-lemma/widget/lemma_content/mainContent/lemmaRelation/lemmaRelation_ac86a59.css |
| 3    | http://www.baidu.com/                    |
| ...  | ...                                      |
| 78   | https://bkssl.bdimg.com/static/wiki-lemma/lemmaCode/script/shBrushPython_40891a8.js |
| 79   | https://bkssl.bdimg.com/static/wiki-lemma/widget/tools/announcement/announcement_126f5e6.css |

### 六、主要函数

- ```python
  def read(url):#读取网页
  ```


- ```python
  def getTitle(html):#获取网页标题
  ```


- ```python
  def getLinks(html):  #获取网页里所有的链接地址
  ```


- ```python
  def nsfile(html):#将爬取到的网页以TXT形式存放到指定目录下
  ```


- ```python
  def getDocSize(path):# 获取文件大小
  ```


- ```python
  def getmysql(title,size,link):#连接数据库并存储
  ```


- ```python
  if __name__ == '__main__':#主函数
  ```


