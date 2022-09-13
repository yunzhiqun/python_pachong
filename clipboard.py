# -*- codeing: utf-8 -*-
# @Time :2022/7/6 10:58
# @Author :shilingming
# @Site :
# @File :clipboard.py.py
# @Software: PyCharm


import win32con
from PIL import Image
import win32clipboard as w
from io import BytesIO
from urllib import request

# 读取本地图片内容
def getLocalImageData(path):
    img = Image.open(path)
    output = BytesIO()  # BytesIO实现了在内存中读写bytes
    img.convert("RGB").save(output, "BMP") #以RGB模式保存图像
    data = output.getvalue()[14:]
    output.close()
    return data

# 读取互联网远程的图片内容
def getNetImageData(netUrl):
    file = BytesIO(request.urlopen(netUrl).read())
    img = Image.open(file)
    output = BytesIO()  # BytesIO实现了在内存中读写bytes
    img.convert("RGB").save(output, "BMP") #以RGB模式保存图像
    data = output.getvalue()[14:]
    output.close()
    return data

# 把 Pillow/PIL Image object 塞入剪贴板
def getPILImageData(img):
    output = BytesIO()  # BytesIO实现了在内存中读写bytes
    img.convert("RGB").save(output, "BMP") #以RGB模式保存图像
    data = output.getvalue()[14:]
    output.close()
    return data

# 把图片内容塞入剪贴板
def setImageDataToClipboard(data):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_DIB, data)
    w.CloseClipboard()
