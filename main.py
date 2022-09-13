# -*- codeing': 'utf-8 -*-
# @Time :2022/5/24 10:53
# @Author :shilingming
# @Site :
# @File :main.py
# @Software': 'PyCharm

# import bs4      #网页解析，获取数据
import os
import uuid

import pyperclip
from bs4 import BeautifulSoup
import win32con
import re       #正则表达式，进行文字匹配
import urllib.request,urllib.error #定制url,获取网页数据
import xlwt     #进行excel操作
# import sqlite3 #进行sqlite数据库操作
import datetime
# import numpy as np
# # 导入 pandas 和 matplotlib
import pandas as pd
import matplotlib.pyplot as plt

import math
import time
from matplotlib.pyplot import MultipleLocator
# import write_excel_to_db
import Db
# pip install pillow, 用Image模块操作图片文件
from PIL import Image

# BytesIO是操作二进制数据的模块
from io import BytesIO

# pip install pywin32, win32clipboard是操作剪贴板的模块
import win32clipboard
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签SimHei
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
plt.rcParams['figure.figsize']=(12.8, 7.2)
#绘图的xy轴数据对应列 
x=6
y=1

#爬取时间跨度
before_len = 3
#展示时间跨度
show_time_len = 30
title_head = "2022年汇率波动"
# title_head = "近一月汇率波动"
# before_len = 7
# title_head = "近一周汇率波动"

begin_date = '2022-01-01'
#表头列表
# excel_head_list = ["货币名称","现汇买入价","现钞买入价","现汇卖出价","现钞卖出价","中行折算价","发布时间"]
excel_head_list = []
#获取当前日期
now_time=datetime.datetime.now().strftime('%Y-%m-%d')
start_time = (datetime.datetime.now()+datetime.timedelta(days=-before_len)).strftime('%Y-%m-%d')
# baseurl1 = "https://srh.bankofchina.com/search/whpj/search_cn.jsp?erectDate="+start_time+"&nothing="+now_time+"&pjname=%E8%8B%B1%E9%95%91" 
# baseurl2 = "&head=head_620.js&bottom=bottom_591.js"
savepath = ".\\chart_pic\\"+now_time+"_汇率.xls" 
save_picture_path = ".\\chart_pic\\"+now_time+"_汇率.jpg" 
save_table_path = ".\\chart_pic\\"+now_time+"_history.jpg" 
db_name_list = ['type','xianhui_buy','xianchao_buy','xianhui_sale','xianchao_sale','zhesuan_price','id','time']
# def main():   
#     #1，获取网页数据
#     #2，解析网页数据(边获取边解析)
#     datalist = getDate(baseurl1,baseurl2)  
#     # 保存获取数据
#     saveData(savepath,datalist)
#获取网页数据
def getDate(baseurl1,baseurl2):
    datalist = []
    #获取数据页数和表头
    map = getPage_Head(baseurl1,baseurl2)
    while map['wait']:
        time.sleep(120)
        print("操作频繁，等两分钟")
        map = getPage_Head(baseurl1,baseurl2)
    page = map['page']
    head_list = map['head_list']
    datalist.append(head_list)

    #获取网页数据
    content_list = []
    for i in range(1,int(page)+1):
        url = baseurl1+"&page="+str(i)+baseurl2
        html = askURL(url)
        # print(html)
        #2，解析网页数据
        soup = BeautifulSoup(html,"html.parser")
        
        # # 获取汇率表头 货币名称 现汇买入价 现钞买入价 现汇卖出价 现钞卖出价 中行折算价 发布时间
        # head_list = []
        
        # for th in soup.find_all('th'): 
        #     th_str = th.string.strip().replace('\n', '').replace('\r', '')
        #     if len(th_str) > 0:
        #         head_list.append(th_str)
        # print("head_list")
        # print(head_list)
        # datalist.append(head_list)
        for item in soup.find_all('div',class_="BOC_main publish"):
            for tr in item.find_all('tr'):
                row_list = [] 
                for td in tr.find_all('td'): 
                    td_str = td.string.strip().replace('\n', '').replace('\r', '')
                    if len(td_str) > 0:
                        # content_list.append(td_str)  
                        row_list.append(td_str)
                if len(row_list) > 0:
                    content_list.append(row_list)
    if len(content_list) > 0:
        # print("content_list")
        # print(content_list) 
        content_list = sorted(content_list, key = lambda content_list:get_list(content_list[x]))
        datalist.extend(content_list)
    return datalist
    
#日期转时间戳便于比较大小
def get_list(date):    
    # 先转换为时间数组
    timeArray = time.strptime(date, "%Y.%m.%d %H:%M:%S") 
    # 转换为时间戳
    timeStamp = int(time.mktime(timeArray))
    return timeStamp 

#获取数据页数和表头
def getPage_Head(baseurl1,baseurl2):
    #获取网页数据
    html = askURL(baseurl1+baseurl2)

    map = {}

    wait = False
    if '您的查询操作太频繁，请一分钟后再试' in html:
        wait = True
    if not wait:
        # print(html)
        #2，解析网页数据
        soup = BeautifulSoup(html,"html.parser")
        # 获取汇率表头 货币名称 现汇买入价 现钞买入价 现汇卖出价 现钞卖出价 中行折算价 发布时间
        head_list = []
        
        for th in soup.find_all('th'): 
            th_str = th.string.strip().replace('\n', '').replace('\r', '')
            if len(th_str) > 0:
                head_list.append(th_str)
        # div_list = soup.find_all('div',class_='turn_page')
        # ol_list = div_list[0].find_all('ol')
        # li_list = ol_list[0].find_all('li')
        # page = re.findall(r'\d+',li_list[0].string) 
        regex1 = '(?<=var m_nRecordCount = ).[0-9]*'
        regex2 = '(?<=var m_nPageSize = ).[0-9]*'
        m_nRecordCount = re.findall(regex1, html)
        m_nPageSize = re.findall(regex2, html)
        page = math.ceil(int(m_nRecordCount[0])/int(m_nPageSize[0]))
        # print("page")
        # print(page)
        
        map['head_list'] = head_list
        map['page'] = page
    map['wait'] = wait
    return map

#得到指定url的网页内容
def askURL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53 sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101" sec-ch-ua-mobile: ?0 sec-ch-ua-platform: "Windows"'
    }

    request = urllib.request.Request(url,headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

#3，提取数据
def saveData(savepath,datalist):
    
    #创建excel
    workbook = xlwt.Workbook(encoding="utf-8") #创建工作簿
    worksheet = workbook.add_sheet("汇率") #创建工作表
    # worksheet.write(0,0,now_time)
    # print(datalist)
    #写入excel
    for i in range(len(datalist)):
        # print(datalist[i])
        for j in range(len(datalist[i])):
            # print(datalist[i][j])
            # worksheet.write(i+1,j,datalist[i][j])
            if(is_number(datalist[i][j])):
                worksheet.write(i,j,float(datalist[i][j]))
            else:
                worksheet.write(i,j,datalist[i][j])
    workbook.save(savepath)
    print("保存成功")
    x_values = []
    y_values = []  
    for i in range(len(datalist)-1): 
        # if (i>0 and i<len(datalist)-1 and datalist[i+1][x]!=datalist[i][x]) or i==len(datalist)-1 or i==0: 
        x_values.append(datalist[i+1][x])   #折线图的x轴数据
        y_values.append(float(datalist[i+1][y]))   #折线图的y轴数据
    # plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
    x_values = pd.to_datetime(x_values)
    
    #设置间隔
    y_major_locator=MultipleLocator(2)
    ax=plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)

    #去除边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    #纵坐标最值
    min_item = math.floor(min(y_values)) 
    max_item = math.ceil(max(y_values)) 
    #设置纵坐标范围
    plt.ylim((min_item-4, max_item+2))

    #添加横向辅助线
    plt.grid(axis="y",ls=":")#打开坐标网格
    plt.title(title_head)
    # plt.axhline(x=0,ls=":",c="yellow")#添加水平直线

    plt.plot(x_values,y_values,color='blue',alpha=0.8,linewidth=3, label="汇率")
    # 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
    plt.legend(loc="upper right")
    plt.xlabel(datalist[0][x])
    plt.ylabel(datalist[0][y])
    
    #显示今天最近一次的数据
    today_x = datalist[len(datalist)-1][x]
    today_y = float(datalist[len(datalist)-1][y])
    plt.text(datetime.datetime.strptime(today_x, "%Y.%m.%d %H:%M:%S"),today_y,today_y, size=12,verticalalignment='bottom' ,horizontalalignment='left',color='b')

    plt.savefig(save_picture_path)  # 保存该图片 
    # plt.show()
    print("绘图成功")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

#数据放入数据库
def saveToMysql(data,con):
    # con = Db.connect_mysql()
    #插入数据库
    for i in range(1,len(data)):
        db_name = ""
        excel_val = ""
        select_sql = "select * from exchange_rate where id = '"+str(data[i][len(data[i])-1]) +"'"
        select_data = Db.select_mysql(con,select_sql)
        if len(select_data) == 0:
            for j in range(len(data[i])):
                db_name += db_name_list[j] + ',' 
                excel_val += '\''+str(data[i][j]) + '\''+ ',' 
            db_name += str(db_name_list[len(data[i])])  
            excel_val += '\''+str(data[i][len(data[i])-1]) + '\''
            insert_sql = 'insert into exchange_rate (%s) values (%s)' % (db_name,excel_val) #拼接sql语句 
            # print(insert_sql) 
            Db.insert_mysql(con,insert_sql)
    print("共插入"+str(len(data)-1)+"条数据")
    # Db.close_mysql(con)

#展示数据
def showData(datalist,con): 
    x_values = []
    y_values = []  
    for i in range(len(datalist)): 
        # if (i>0 and i<len(datalist)-1 and datalist[i+1][x]!=datalist[i][x]) or i==len(datalist)-1 or i==0: 
        x_values.append(datalist[i][x])   #折线图的x轴数据
        y_values.append(float(datalist[i][y]))   #折线图的y轴数据
    # plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
    x_values = pd.to_datetime(x_values)
    
    #设置间隔
    y_major_locator=MultipleLocator(2)
    ax=plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)

    #去除边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    #纵坐标最值 
    min_item = math.floor(min(y_values)) 
    max_item = math.ceil(max(y_values)) 
    min_item_x = y_values.index(min(y_values))
    max_item_x = y_values.index(max(y_values))
    #设置纵坐标范围
    plt.ylim((min_item-4, max_item+2))

    #添加横向辅助线
    plt.grid(axis="y",ls=":")#打开坐标网格
    plt.title(title_head)
    # plt.axhline(x=0,ls=":",c="yellow")#添加水平直线

    plt.plot(x_values,y_values,color='blue',alpha=0.8,linewidth=3, label="汇率")
    # 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
    plt.legend(loc="upper right")

    #查询数据库表格表头
    select_sql = "select name from exchange_rate_excel_head order by id"
    select_data = Db.select_mysql(con,select_sql)
    #设置横纵坐标名称
    plt.xlabel(select_data[x][0])
    plt.ylabel(select_data[y][0])
    
    #显示今天最近一次的数据
    today_x = datalist[len(datalist)-1][x]
    today_y = float(datalist[len(datalist)-1][y]) 
    
    plt.text(today_x,today_y,today_y, size=12,verticalalignment='bottom' ,horizontalalignment='left',color='b')
    #标注最大值最小值    
    if min_item != today_y:
        min_x_value = datalist[min_item_x][x]
        min_plt = plt.text(min_x_value,min_item,min_item, size=12,verticalalignment='top' ,horizontalalignment='left',color='b')

    if max_item != today_y:
        max_x_value = datalist[max_item_x][x]
        max_plt = plt.text(max_x_value,max_item,max_item, size=12,verticalalignment='top' ,horizontalalignment='left',color='b')
 
    # print(save_picture_path)
    plt.savefig(save_picture_path)  # 保存该图片 
    #历史最高最低复制到剪切板 
    max_data = get_history_max_min(con,True)
    min_data = get_history_max_min(con,False)
    max_txt = ""
    for i in range(len(max_data)):
        max_txt += max_data[i][1] + "：" + str(max_data[i][0]) + "\n" 
    min_txt = ""
    for i in range(len(min_data)):
        min_txt += min_data[i][1] + "：" + str(min_data[i][0]) + "\n" 
    text_history = "历史最高：\n"+max_txt+"历史最低：\n"+min_txt+"最新汇率：\n"+now_time+ "：" +str(today_y)
    pyperclip.copy(text_history)  
    send_msg_to_clip(win32con.CF_UNICODETEXT, text_history,True) 
    #图片复制到剪切板
    # max_list = []
    # min_list = []
    # max_list.append(data[0][0])
    # min_list.append(data[0][1])

    # create_table_img(max_list, min_list, save_table_path)
    # paste_img(save_table_path,True)

    #图片复制到剪切板
    paste_img(save_picture_path,False)

    plt.close()
    # plt.show()
    print("绘图成功")

 
#获取数据库历史最高最低值
def get_history_max_min(con,is_max):
    #查询语句
    value_name = db_name_list[y]
    time_name = db_name_list[x]
    sql = ""
    # sql = "select MAX("+value_name+") max_history, ,MIN("+value_name+") min_history from exchange_rate " 
    if is_max:
        sql = "select DISTINCT "+value_name+" max_val , DATE_FORMAT(" + time_name + " ,'%Y-%m-%d') date  from exchange_rate WHERE  "+value_name+"  =(select MAX( "+value_name+" ) from exchange_rate) "
    else:
        sql = "select DISTINCT "+value_name+" min_val , DATE_FORMAT(" + time_name + " ,'%Y-%m-%d') date from exchange_rate WHERE  "+value_name+"  =(select MIN( "+value_name+" ) from exchange_rate) "
    # print(sql) 
    #查询数据
    data = Db.select_mysql(con,sql) 
    return data
#复制图片到剪切板
# 操作剪贴板分四步：
# 1. 打开剪贴板：OpenClipboard()
# 2. 清空剪贴板，新的数据才好写进去：EmptyClipboard()
# 3. 往剪贴板写入数据：SetClipboardData()
# 4. 关闭剪贴板：CloseClipboard()
# :param type_data: 数据的格式，
# unicode字符通常是传 win32con.CF_UNICODETEXT
# :param msg: 要写入剪贴板的数据
def send_msg_to_clip(type_data, msg,is_clear):
    try:
        win32clipboard.OpenClipboard()
        if is_clear:
            win32clipboard.EmptyClipboard() # 清空剪贴板
        win32clipboard.SetClipboardData(type_data, msg)
        win32clipboard.CloseClipboard()
    except:
        raise ValueError('剪切板被其他程序锁定')
    

# 图片转换成二进制字符串，然后以位图的格式写入剪贴板
# 主要思路是用Image模块打开图片，
# 用BytesIO存储图片转换之后的二进制字符串
# :param file_img: 图片的路径
def paste_img(file_img,is_clear): 
    # 把图片写入image变量中
    # 用open函数处理后，图像对象的模式都是 RGB
    image = Image.open(file_img)
    # 声明output字节对象
    output = BytesIO()
    # 用BMP (Bitmap) 格式存储
    # 这里是位图，然后用output字节对象来存储
    image.save(output, 'BMP')
    # BMP图片有14字节的header，需要额外去除
    data = output.getvalue()[14:]
    # 关闭
    output.close()
    # DIB: 设备无关位图(device-independent bitmap)，名如其意
    # BMP的图片有时也会以.DIB和.RLE作扩展名
    # 设置好剪贴板的数据格式，再传入对应格式的数据，才能正确向剪贴板写入数据
    send_msg_to_clip(win32clipboard.CF_DIB, data,is_clear)
#查找缺失日期
def findMissingDate(begin_time,con):
    #mysql统计两日期中间缺失日期
    check_sql = "select DATE_FORMAT(time,'%Y-%m-%d') date FROM exchange_rate WHERE time > '"+begin_date+"' GROUP BY date" 
    # con = Db.connect_mysql()
    check_data = Db.select_mysql(con,check_sql) 
    # Db.close_mysql(con)
    lost_data = get_no_date(check_data, begin_time, now_time) 
    # print("缺失日期："+str(lost_data))
    return lost_data

#  获取没有列表中没有包含的的⽇期区间的⽇期
# args:
#     start_date: 查询的起始⽇期字符串，默认为date_li中最⼩值
#     end_date: 查询的终⽌⽇期的字符串, 默认为date_li中最⼤值
#     date_str_li：所有需要查询的⽇期的列表 
def get_no_date(date_str_li, start_date='', end_date=''): 
    if not date_str_li:
        raise ValueError('list can\'t empty')
    # 所有⽂件名称，⽇期的列表  
    try:
        date_li = [datetime.datetime.strptime(date_time[0], '%Y-%m-%d') for date_time in date_str_li]
    except:
        raise ValueError('your values can\'t  be converted')
    if end_date:
        date_end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    else:
        date_end = max(date_li)
    if start_date:
        date_start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    else:
        date_start = min(date_li)
    no_list = []
    while True:
        if date_end not in date_li:
            no_list.append(date_end)
        if date_end == date_start:
            break
        date_end -= datetime.timedelta(1)
    return [datetime.date.strftime(day, '%Y-%m-%d') for day in no_list] 

#查询数据库中 begin_date 到 now_time 的数据,如有缺失，则查询并写入数据库 
def get_save_data(con): 
    lost_data = findMissingDate(begin_date,con)
    #如果存在缺失日期，则爬取数据
    if len(lost_data) > 0: 
        for date in lost_data: 
            baseurl1 = "https://srh.bankofchina.com/search/whpj/search_cn.jsp?erectDate="+date+"&nothing="+date+"&pjname=%E8%8B%B1%E9%95%91" 
            baseurl2 = "&head=head_620.js&bottom=bottom_591.js"
            #等待一段时间，防止爬取过快导致服务器拒绝访问
            print("等待5s后爬取"+date+"日数据") 
            time.sleep(5) 
            #获取数据
            datalist = getDate(baseurl1,baseurl2)  
            print(date+"数据爬取完成")
            #更新表头

            #存入数据库
            saveToMysql(datalist,con)
            print(date+"数据存入数据库") 

#查询绘图数据
def get_draw_data(con): 
    #查询字段
    db_name = ''
    for j in range(len(db_name_list)-1):
        db_name += db_name_list[j] + ',' 
    db_name = db_name[0:len(db_name)-1]
    #查询日期
    search_begin_time = (datetime.datetime.now()+datetime.timedelta(days=-show_time_len)).strftime('%Y-%m-%d')
    # where = "where time > '"+ search_begin_time +"'"
    where = "where time > '2022-01-01'"
    #查询语句
    sql = "select "+db_name+" from exchange_rate " + where
    # print(sql)
    #打开数据库
    # con = Db.connect_mysql()
    #查询数据
    data = Db.select_mysql(con,sql) 
    return data


def update_table_head(datalist,con):
    select_sql = "select id from exchange_rate_excel_head"
    head_id_list = Db.select_mysql(con,select_sql)
    
    #更新表头
    for i in range(len(datalist[0])):
        if i == 0:
            continue
        else:
            if len(head_id_list) > 0: 
                sql = "update exchange_rate set name = "+str(datalist[0][i])+" where id = '"+head_id_list[i]+"'"
                Db.update_mysql(con,sql)
            else:
                #新增表头
                sql = "insert into exchange_rate_excel_head(name) values("+str(datalist[0][i])+")"
                Db.insert_mysql(con,sql)

# if __name__ == "__main__":
#     data = {
#         "Books": [29, 23, 29, 20, 25, 23, 26],
#         "Magazines": [26, 23, 29, 28, 24, 22, 29], }
def create_table_img(history_max,history_min,path):
    data = {}
    data['max'] = history_max
    data['min'] = history_min
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(3, 4))
    ax.axis("off")
    ax.axis("tight")
    tb = ax.table(cellText=df.values, colLabels=df.columns, bbox=[0, 0, 1, 1], )
    tb[0, 0].set_facecolor("lightblue")
    tb[0, 1].set_facecolor("lightblue")
    tb[0, 0].set_text_props(color="black")
    tb[0, 1].set_text_props(color="black") 
    # plt.show()
    # 保存图片
    plt.savefig(path)
#运行程序
def run():
    con = Db.connect_mysql()
    #查询数据库中 begin_date 到 now_time 的数据,如有缺失，则查询并写入数据库 
    get_save_data(con) 
    #查询绘图数据
    data = get_draw_data(con)
    #根据data绘图
    showData(data,con)  
    #关闭数据库
    Db.close_mysql(con)
if __name__ == '__main__':
    # lost_data = findMissingDate(begin_date)
    # print(lost_data)
    # 检查今天数据是否为空，空则爬取数据加入数据库，否则跳过
    # con = Db.connect_mysql()
    # check_sql = "select * from exchange_rate where time > '"+now_time +"'"
    # check_data = Db.select_mysql(con,check_sql)
    # if len(check_data) == 0:
    #     print("今天数据为空，开始爬取数据")
    #     datalist = getDate(baseurl1,baseurl2)  
    #     saveToMysql(datalist)

    con = Db.connect_mysql()
    #查询数据库中 begin_date 到 now_time 的数据,如有缺失，则查询并写入数据库 
    get_save_data(con) 
    #查询绘图数据
    data = get_draw_data(con)
    #根据data绘图
    showData(data,con)  
    #关闭数据库
    Db.close_mysql(con)
    


