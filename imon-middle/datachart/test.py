# -*- coding: utf-8 -*-
import pymysql
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib

def test():
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
    #统计网页数量
    print("已存入数据库的网页数量是：" + str(cursor.execute("select LAST_INSERT_ID() from page")))
    #统计url表中每个域名出现的次数并按降序排列
    cursor.execute("select domains,count(domains) from url group by domains order by count(domains) DESC")
    exdo = cursor.fetchall()
    #将排列结果存入到数据表exdomains中
    for i in exdo:
        name = i[0]
        count = i[1]
        cursor.execute("INSERT INTO exdomains(name,count) VALUES ('%s', %d)" % (name, count))
        conn.commit()
    print("已将结果存入表exdomains中！")
    #网页大小分布
    cursor.execute("select max(size) from page")
    max = cursor.fetchone()[0]#最大的网页size
    cursor.execute("select min(size) from page")
    min = cursor.fetchone()[0]#最小的网页size

    avg = (max-min)/10
    avg = int(avg+1)
    group = []
    x = []#x轴
    y = []#y轴
    for i in range(11):
        group.append(min+avg*i)
    #print(group)
    for i in range(11):
        if i < 10:
            size1 = group[i]
            size2 = group[i+1]
            x.append(str(group[i])+"~"+str(group[i+1]))#构造X轴的表现形式，eg：24360~40597
            #在数据库中查询每段各含有多少个网页
            cursor.execute("select count(*) from page where (size>=%d and size <%d)" % (size1,size2))
            dd = cursor.fetchone()[0]
            y.append(dd)#构造Y轴表现形式
    get_chart(x,y)#分组画柱状图

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

test()