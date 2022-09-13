# -*- codeing: utf-8 -*-
# @Time :2022/6/13 14:38
# @Author :shilingming
# @Site :
# @File :search_m3u8.py
# @Software: PyCharm
from bs4 import BeautifulSoup
import sys
import re       #正则表达式，进行文字匹配
import urllib.request,urllib.error #定制url,获取网页数据
# import easygui
import ssl
import requests
import re
from Crypto.Cipher import AES
ssl._create_default_https_context = ssl._create_unverified_context
def main(input):
    url = input[0]
    html = str(askURL(url))
    soup = BeautifulSoup(html,"html.parser")
    # print(html)
    movie = ''
    for connect in soup.find_all('script', type='text/javascript'):
        temp_link = connect.text.strip().replace('\n', '').replace('\r', '')
        if len(temp_link) > 0 and 'm3u8' in temp_link:
            print(temp_link)
            movie = temp_link
    if len(movie) > 0:
        regex1 = "http[s]?:(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+m3u8"
        movie = re.findall(regex1, movie)
        # print(movie)
        final_url = movie[0]
        if ('/' in final_url) and ('\\' in final_url) :
            final_url = final_url.strip().replace('\\', '')
        if (not ('/' in final_url)) and ('\\' in final_url):
            key = final_url.strip().replace('\\', '/')
        # easygui.textbox(title= 'url包含的文件地址' , text = final_url,msg = 'url包含的文件地址')
        print('输出：',final_url)
        m3u8(final_url)
    else:
        print('没有找到m3u8文件')
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


def m3u8(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # requests得到m3u8文件内容
    content = requests.get(url,headers=header).text
    if "#EXTM3U" not in content:
        print("这不是一个m3u8的视频链接！")
        return False
    if "EXT-X-KEY" not in content:
        print("没有加密")
        return False 
    # 使用re正则得到key和视频地址
    jiami=re.findall('#EXT-X-KEY:(.*)\n',content)
    key=re.findall('URI="(.*)"',jiami[0])
    #得到每一个ts视频链接
    tslist=re.findall('EXTINF:(.*),\n(.*)\n#',content)
    newlist=[]
    for i in tslist:
        newlist.append(i[1])

    
    # 先获取URL/后的后缀，再替换为空  
    urlkey=url.split('/')[-1]
    url2 = url.replace(urlkey, '')  #这里为得到url地址的前面部分，为后面key的链接和视频链接拼接使用

    #得到key的链接并请求得到加密的key值
    keyurl=url2+key[0]
    keycontent= requests.get(keyurl,headers=header).text

    #得到每一个完整视频的链接地址
    tslisturl=[]
    for i in newlist:
        tsurl=url2+i
        tslisturl.append(tsurl)

    #得到解密方法，这里要导入第三方库  pycrypto
    #这里有一个问题，安装pycrypto成功后，导入from Crypto.Cipher import AES报错
    #找到使用python环境的文件夹，在Lib文件夹下有一个 site-packages 文件夹，里面是我们环境安装的包。
    #找到一个crypto文件夹，打开可以看到 Cipher文件夹，此时我们将 crypto文件夹改为 Crypto 即可使用了
    cryptor = AES.new(keycontent, AES.MODE_CBC, keycontent)

    #for循环获取视频文件
    for i in tslisturl:
        res = requests.get(i, header)
        #使用解密方法解密得到的视频文件
        cont=cryptor.decrypt(res.content)
        #以追加的形式保存为mp4文件
        with open('xx.mp4', 'ab+') as f:
            f.write(cont)
    return True

# if __name__ == '__main__':
#     url = "https://vod1.ttbfp2.com/20210813/yee3IjRa/index.m3u8"
#     pd = m3u8(url)
#     if pd:
#       print('视频下载完成！')
if __name__ == '__main__':
    main(sys.argv[1:])
    # url = "https://vod1.ttbfp2.com/20210813/yee3IjRa/index.m3u8"
    # main(url)