# -*- codeing: utf-8 -*-
# @Time :2022/5/24 13:13
# @Author :shilingming
# @Site :
# @File :test_urllib.py
# @Software: PyCharm

import urllib.request
import urllib.parse
def get_qingqiu():
    #获取一个get请求
    response = urllib.request.urlopen('http://www.baidu.com')
    #对获取的网页源码进行utf-8编码
    print(response.read().decode('utf-8'))

#获取一个post请求 通常用于模拟用户登录
def post_qingqiu():
    data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf-8')
    #http://httpbin.org/post 一个用于测试post请求的网址
    try:
        response = urllib.request.urlopen('http://httpbin.org/post',data = data,timeout=0.01) # timeout 设置超时时间
        # response = urllib.request.urlopen('http://httpbin.org/get')
        #对获取的网页源码进行utf-8编码
        print(response.read().decode('utf-8'))
        print(response.status) #获取状态码
        print(response.getheaders) #获取请求头
        print(response.getheader("Server"))  # 获取请求头 Server 的值
    except urllib.error.URLError as e:
        print('超时')

def fake_to_douban_get():
    # url = "https://www.douban.com"
    # headers = {
    #     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    # }
    # data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf-8')
    # req = urllib.request.Request(url=url,data=data,headers=headers,method="POST")
    # response = urllib.request.urlopen(req)
    # print(response.read().decode('utf-8'))
    url = "https://www.douban.com"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf-8')
    req = urllib.request.Request(url=url,headers=headers)
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
if __name__ == '__main__':
    fake_to_douban_get()