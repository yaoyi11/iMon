# -*- coding: utf-8 -*-
import pymysql
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib
import getopt
import sys

def get_cmd():#从命令行读取参数
    config = {"crawl_id":'1'}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:",["crawl_id="])
    except getopt.GetoptError:
       print('test3.py -c <crawl_id>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print('test3.py -c <crawl_id> -o <outputfile>')
          sys.exit()
       elif opt in ("-c", "--crawl_id"):
          config['crawl_id'] = arg
    return config

def get_mysql():#连接数据库
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
    return (cursor, conn)

def get_time(cid):#抓取任务执行了多久
    cursor,co = get_mysql()
    sql = ("SELECT start_time,end_time FROM crawl where cid=%d" % cid)
    cursor.execute(sql)
    jieguo = cursor.fetchone()
    all_time = (jieguo[1] - jieguo[0]).seconds
    print("共执行了"+str(all_time) + "秒")

def get_page(cid):#一共抓了多少个网页/资源
    cursor,co = get_mysql()
    sql2 = ("select LAST_INSERT_ID() from page where cid=%d" % cid)
    page = cursor.execute(sql2)
    print("抓取的网页数："+str(page))
    return page

def get_links(cid):#每个网页平均含有几个链接
    cursor,co = get_mysql()
    sql3 = ("select count from page where cid=%d" % cid)
    cursor.execute(sql3)
    guo = cursor.fetchall()
    results = [i[0] for i in guo]
    avg = int(sum(results) / len(results))
    print("每个网页平均含有"+str(avg)+"个链接")

def get_domains(cid,page):#整个网站一共有多少个外链的域名，每个域名有多少次,将结果存入到数据库exdomains
    cursor,co = get_mysql()
    sql = ("select domains,count(domains) from url where page_id between %d and %d group by domains order by count(domains) DESC" % (cid,page))
    cursor.execute(sql)
    exdo = cursor.fetchall()
    # 将排列结果存入到数据表exdomains中
    for i in exdo:
        name = i[0]
        count = i[1]
        cursor.execute("INSERT INTO exdomains(name,count) VALUES ('%s', %d)" % (name, count))
        co.commit()
    print("已将域名排序结果存入表exdomains中！")
    #print(exdo)

def get_size(cid):#网页的平均大小
    cursor,co = get_mysql()
    sql5 = ("select size from page where cid=%d" % cid)
    cursor.execute(sql5)
    guo1 = cursor.fetchall()
    results1 = [i[0] for i in guo1]
    avg1 = int(sum(results1) / len(results1))
    print("网页的平均大小："+str(avg1)+"b")

def get_pagebar(cid):#网页的大小分布柱状图
    cursor,co = get_mysql()
    cursor.execute("select max(size) from page where cid=%d" % cid)
    max = cursor.fetchone()[0]  # 最大的网页size
    cursor.execute("select min(size) from page where cid=%d" % cid)
    min = cursor.fetchone()[0]  # 最小的网页size
    #print(max,min)
    avg = (max - min) / 10
    avg = int(avg + 1)
    group = []
    x = []  # x轴
    y = []  # y轴
    for i in range(11):
        group.append(min + avg * i)
    # print(group)
    for i in range(11):
        if i < 10:
            size1 = group[i]
            size2 = group[i + 1]
            x.append(str(int(group[i]/1024))+"kb" + "~" + str(int(group[i + 1]/1024))+"kb")  # 构造X轴的表现形式，eg：24360~40597
            # 在数据库中查询每段各含有多少个网页
            cursor.execute("select count(*) from page where (size>=%d and size <%d and cid=%d)" % (size1, size2,cid))
            dd = cursor.fetchone()[0]
            y.append(dd)  # 构造Y轴表现形式
    get_chart(x, y)  # 分组画柱状图

def get_chart(x,y):
    #设置柱状图的字体
    zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\\Windows\\Fonts\\simsun.ttc')
    #x轴标签
    plt.xlabel("size的分组", fontproperties=zhfont1)
    #y轴标签
    plt.ylabel("出现次数", fontproperties=zhfont1)
    #柱状图标题
    plt.title("网页大小分布图", fontproperties=zhfont1)
    plt.bar(range(len(y)), y, tick_label=x)#生成柱状图
    for a, b in zip(range(len(y)), y):
        plt.text(a, b, '%d' % b, ha='center', va='bottom')#添加数据标签
    plt.show()

if __name__ == "__main__":
   config = get_cmd()
   cid = config['crawl_id']
   cid = int(cid)
   get_time(cid)
   page = get_page(cid)
   get_links(cid)
   get_domains(cid, page)
   get_size(cid)
   get_pagebar(cid)

