# -*- codeing: utf-8 -*-
# @Time :2022/6/27 9:11
# @Author :shilingming
# @Site :
# @File :QrCode2Link.py.py
# @Software: PyCharm

from PIL import Image, ImageGrab
import os
import cv2#导入opencv库
import pyperclip
#二维码转链接
def qrCode2Link(): 
    getClipboardImg()
    img=cv2.imread("qrcode.png")#打开二维码图片
    det=cv2.QRCodeDetector()#创建二维码识别器
    val, pts, st_code = det.detectAndDecode(img)#识别二维码
    # print(val)#打印识别出的链接 
    text2Clipboard(val)
    #删除图片
    os.remove("qrcode.png")

#获取剪切板图片
def getClipboardImg(): 
    # 保存剪切板内图片
    img = ImageGrab.grabclipboard()
    img.save("qrcode.png")
    return img
    
#文本复制到剪切板
def text2Clipboard(text): 
    pyperclip.copy(text)
    print("已复制到剪切板")
 
if __name__ == '__main__':
    qrCode2Link()