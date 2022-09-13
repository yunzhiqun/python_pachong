# -*- codeing: utf-8 -*-
# @Time :2022/7/17 22:07
# @Author :shilingming
# @Site :
# @File :xiangsheng_pachong.py.py
# @Software: PyCharm

import os
import ssl
import tkinter
# 导入消息对话框子模块
import tkinter.messagebox 
from bs4 import BeautifulSoup
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 定制url,获取网页数据
import Db
import gzip

# 得到指定url的网页内容
def askURL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53 sec-ch-ua: " Not A;Brand";v="99", '
                      '"Chromium";v="101", "Microsoft Edge";v="101" sec-ch-ua-mobile: ?0 sec-ch-ua-platform: "Windows" '
    }

    request = urllib.request.Request(url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        # 网页的 charset明明是GB2312 微软将 gb2312 和 gbk 统一映射为 gb18030
        html = response.read().decode("gb18030") 
        # html = response.read().decode("ISO-8859-1") 
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 解析页面每页url
def get_page_url(url):
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    page_url = []
    for item in soup.find_all('div', class_="list_page"):
        for a in item.find_all('a', href=True):
            href_str = a.get('href') 
            if len(href_str) > 0:
                page_url.append(href_str)
    return list_duplicate(page_url)


# 解析页面的音频列表
def get_audio_list(url):
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    audio_list = []
    for item in soup.find_all('div', class_="index_middle"):
        for ul in item.find_all('ul'):
            for a in ul.find_all('a', href=True):
                href_str = a.get('href')
                if len(href_str) > 0:
                    audio_list.append(href_str)

    return audio_list


# 解析详情页面音频下载地址 url title 数据库id
def get_audio_url(main_url, url_detail):
    url = connect_str_del_useless(main_url, url_detail)
    html = askURL(url)

    # 正则表达式提取音频下载地址
    regex_mp3 = r'mp3: "(.+?)\"'
    audio_url = re.findall(regex_mp3, html)
    soup = BeautifulSoup(html, "html.parser")

    regex_title = r'title: "(.+?)\"'
    audio_title = re.findall(regex_title, html)
    if len(audio_title) > 0:
        audio_title[0] = validateTitle(audio_title[0])
    detail = []
    if len(audio_url) > 0 and len(audio_title) > 0:
        detail = [audio_url[0], audio_title[0], get_id(url)]
    else:
        print("解析音频地址失败")
        print(url)
        print(html)
        detail = ['', '', '']
    return detail


# 解析并下载音频
def get_download_audio(url, file_path, con):
    
    # 获取指定url的音频列表
    audio_list = get_audio_list(url)
    # 获取指定url的音频详情
    for audio in audio_list:
        audio_detail = get_audio_url(url, audio)
        if audio_detail[0] != '' and audio_detail[1] != '' and audio_detail[2] != '':
            detail_url = audio_detail[0]
            title = audio_detail[1]
            id = audio_detail[2]

            # 拼接完整下载到本地的路径
            suffix = ''
            if url.find('.') > 0:
                suffix = '.'+detail_url.split('.')[-1]  
            absolute_path = file_path +'\\'+ title + suffix
            absolute_path = absolute_path.replace('\\','/')
            can_down = check_url(detail_url)

            if is_exist(id, con):
                print(id + " 数据已存在")
                if can_down:
                    down(id, detail_url,absolute_path)
                
            else: 
                can_down_str = 1
                if can_down:
                    can_down_str = 0
                sql = "insert into xiangsheng(id,title,url,file_path,can_down) values('" + id + "','" + title + "','" + detail_url + "','" + absolute_path + "'" + "," + str(can_down_str) + ")"
                Db.insert_mysql(con, sql)
                print(id + " 数据写入数据库完成")
                down(id, detail_url,absolute_path)

        # 下载音频文件
        # file_path = os.getcwd()  # 当前工作目录。
        # down_file(audio_detail[0],audio_detail[1],file_path)
        # 插入数据库
    


# 根据url下载音频文件到指定目录
def down_file(url, absolute_path): 
    try:
        urllib.request.urlretrieve(url, absolute_path)  # 下载文件 
    except: 
        print("下载失败")
        print(url)
        print(absolute_path) 

    

# 查询数据是否已经存在数据库中
def is_exist(id, con):
    sql = "select * from xiangsheng where id = '" + id + "'"
    data = Db.select_mysql(con, sql)
    if len(data) > 0:
        return True
    else:
        return False

# 检查url是否可下载
def check_url(url):
    context = ssl._create_unverified_context()
    #如果不是url，则返回False
    if not url.startswith('http'):
        return False
    else:
        try:
            # 如果url可以下载，先把后面的rpc截取掉，再进行校验是否可下载
            response = urllib.request.urlopen(url, context=context)
            return True
        except: 
            #如果异常返回false，表示连接失败 
            print(url+"可下载性检查失败")
            return False

# 查询文件是否已下载
def is_down(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False
# 替换文件名不合法字符
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |' 
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title 

# 列表去重
def list_duplicate(list):
    new_list = []
    for item in list:
        if item not in new_list:
            new_list.append(item)
    return new_list


# 下载
def down(id, detail_url,absolute_path):
    if is_down(absolute_path):
        print(id + " 文件已下载")
    else:
        down_file(detail_url,absolute_path)
        print(id + " 文件下载完成")


# 连接两个字符串并去除首尾重复子串
def connect_str(s1, s2):
    length1 = len(s1)
    length = min(length1, len(s2))
    k = max(range(0, length + 1), key=lambda i: i if s1[length1 - i:] == s2[:i] else False)
    return s1 + s2[k:]
    # for i in range(1, len(s2)):
    #     if s1.endswith(s2[:i]):
    #         break
    # return s1 + s2[i:]


# 分割网址，提取关键词，作为数据库id
def get_id(url):
    url_str = url.strip('.html')
    url_list = url_str.split('/')
    id = url_list[len(url_list) - 2] + '_' + url_list[len(url_list) - 1]
    return id


# 创建文件夹，判断文件夹是否存在，不存在则创建
def create_dir(dir):
    if os.path.exists(dir):
        print(dir + "文件夹已存在")
    else:
        os.makedirs(dir)


def main(url, file_path):
    page_list = get_page_url(url) 
    # 打开数据库连接
    con = Db.connect_mysql() 
    #下载首页音频
    get_download_audio(url, file_path, con)
    #下载其他页音频
    for page_url in page_list:
        complete_url = connect_str_del_useless(url, page_url)
        get_download_audio(complete_url, file_path, con)
    # 关闭数据库连接
    Db.close_mysql(con)
# 拼接网址 并去除无用部分
def connect_str_del_useless(str1, str2):
    list1 = str1.split('/')
    list2 = str2.split('/')
    public_str_list = list(set(list1).intersection(set(list2))) 
    public_str = ''
    for item in public_str_list:
        if item != '':
            public_str = item
    if len(public_str) > 0:
        # start = str1.find(str_1)
        public_str = '/'+public_str 
        str1, sep, tail  = str1.partition(public_str) 
    # print(str1+str2)
    return str1 + str2

 #弹出完成提示窗口
def show_message_ok(root):
    root.withdraw() 		 #****实现主窗口隐藏
    tkinter.messagebox.showinfo(title = '相声',message='爬取完成')

if __name__ == '__main__':
    # 爬取的网址
    url = 'http://www.tingdegang.com/kengwang/'
    # 保存的目录
    file_path = os.getcwd()  # 当前工作目录。 
    file_path = file_path + '\\kengwang'
    #创建文件夹
    create_dir(file_path)
    #爬取文件
    main(url, file_path)
    # url2 = '/qiandao/123123.html'
    # connect_str_del_useless(url, url2)

        # 创建主窗口
    #窗口置顶
    root = tkinter.Tk()
    root.wm_attributes('-topmost', 1)  
    show_message_ok(root) # 弹出完成提示窗口




