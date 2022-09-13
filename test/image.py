# -*- codeing: utf-8 -*-
# @Time :2022/6/7 9:15
# @Author :shilingming
# @Site :
# @File :image.py
# @Software: PyCharm

import cv2
import matplotlib.pyplot as plt
from skimage import io
import math
import numpy as np
import os
import copy
from PIL import Image
import tkinter.filedialog

depth = 2  # 0-100,越高，颜色越深


#读取图片
def read_image(path):
    img_1 = cv2.imdecode(np.fromfile(path,dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    # img_1 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # img_1 = img_1 / 255.0
    return img_1

def dispose_image_pil(filename,add_name):
    root = tkinter.Tk().withdraw()
    try:
        # depth = 3  # 0-100,越高，颜色越深
        picture_grad = np.gradient(np.asarray(Image.open(filename).convert('L')).astype('int'))  # 取图像灰度的梯度值
        grad_x, grad_y = picture_grad[0] * depth / 100., picture_grad[1] * depth / 100.  # 将获取的维度梯度值进行深度处理
        base = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)  # 降噪基
        _x, _y, _z = grad_x / base, grad_y / base, 1. / base
        sce_z, sce_x = np.pi / 2.1, np.pi / 3  # 光源的俯视角度值和方位角度值
        # 光源对x,y,z 轴的影响
        dx, dy, dz = np.cos(sce_z) * np.cos(sce_x), np.cos(sce_z) * np.sin(sce_x), np.sin(sce_z)
        Normalized = 255 * (dx * _x + dy * _y + dz * _z).clip(0, 255)  # 光源归一化
        im = Image.fromarray(Normalized.astype('uint8'))  # 重构图像


        
        (file_name, ext) = os.path.splitext(path)
        fin_path = file_name + add_name + ext
        print(fin_path)
        im.save(fin_path)  # 保存转换后的图片
        im.show()  # 展示转换后的图片
    except Exception:
        print('转换失败！')
#最小值滤波
def min_filter(img):
    # 创建一个掩码
    mask = np.zeros(img.shape, dtype=np.uint8)
    # 填充掩码
    mask[1:-1, 1:-1] = 1
    # 对图像进行最小值滤波
    res = cv2.filter2D(img, -1, mask) 
    return res
def dispose_image_opencv(img_path):
    # img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    img = cv2.imread(img_path)
    #去色
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #取反
    inv = 255 - gray

    blur = cv2.GaussianBlur(inv, ksize=(15, 15), sigmaX=50, sigmaY=50)
    # blur = min_filter(inv)
    save_image(blur, path,'_cvminfinal')
    #颜色减淡混合
    res = cv2.divide(gray, blur, scale=255)
    save_image(res, path,'_cvfinal')
#保存图片
def save_image(img,path,add_name):
    (file_name, ext) = os.path.splitext(path)
    fin_path = file_name+add_name+ext
    print(fin_path)
    cv2.imwrite(fin_path, img)
    # cv2.imencode(ext, img)[1].tofile(fin_path)
if __name__ == '__main__':
    # main()
    # path = 'D://ps_image//tuzi.jpg'
    path = tkinter.filedialog.askopenfilename()  # 打开选择文件对话框

    dispose_image_pil(path,'_pilfinal')

    # img = dispose_image_opencv(path) 
    # save_image(img, path,'_cvfinal')