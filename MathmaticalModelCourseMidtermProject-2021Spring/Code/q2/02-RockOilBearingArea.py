# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# author:ygj time:2021/3/27


import cv2 as cv
import numpy as np
import glob
import re


# 岩石边缘提取：返回 岩石像素个数 和 岩石范围图像
def rockAreaDetect(img):
    # 边缘检测
    edges = cv.Canny(img, 150, 750)
    # 开运算
    kernel = np.ones((25, 25), np.uint8)
    opening = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)
    # 计数
    area = 0
    height, width = opening.shape
    # 若为bmp图片，不进行边缘提取
    if height > 512:
        return height * width, img
    for h in range(height):
        for w in range(width):
            if opening[h, w] == 255:
                area += 1
    return area, opening


# 油气范围提取：返回 油气像素个数 和 油气范围图像
def OilAreaDetect(img):
    mask = HSVmask(img)

    # 核
    kernel1 = np.ones((1, 2), np.uint8)
    kernel2 = np.ones((2, 2), np.uint8)
    # 扩张
    dilation = cv.dilate(mask, kernel1, iterations=3)
    # 开运算
    opening = cv.morphologyEx(dilation, cv.MORPH_OPEN, kernel2)
    # 计数
    area = 0
    height, width = opening.shape
    for h in range(height):
        for w in range(width):
            if opening[h, w] == 255:
                area += 1
    return area, opening


# 油气的HSV阈值颜色过滤
def HSVmask(img):
    # HSV阈值
    H_min, S_min, V_min = [0, 43, 46]
    H_max, S_max, V_max = [77, 255, 255]
    # H_min, S_min, V_min = [0, 43, 0]
    # H_max, S_max, V_max = [75, 255, 255]
    lower_hsv = np.array([H_min, S_min, V_min])
    upper_hsv = np.array([H_max, S_max, V_max])

    # 过滤
    mask = cv.inRange(img, lower_hsv, upper_hsv)
    return mask


# Trackbar callback function
def nothing(x):
    pass


# 数据集目录
rootpath = r".\b_data\rock_data"
img1paths = rootpath + "\*-1.*"
img2paths = rootpath + "\*-2.*"

if __name__ == "__main__":
    rockOilBearingArea = {}
    # img1path 和 img2path为 岩石图像 和 油气图像
    for img1path, img2path in zip(glob.glob(img1paths), glob.glob(img2paths)):
        img1 = cv.imread(img1path, cv.COLOR_RGB2HSV)
        img2 = cv.imread(img2path, cv.COLOR_RGB2HSV)

        # 岩石提取及油气提取
        rockarea, rock = rockAreaDetect(img1)
        oilarea, oil = OilAreaDetect(img2)

        # 计算含油面积百分含量
        pattern = '[0-9]+'
        mat = re.search(pattern, img1path, flags=0)
        name = mat.group(0)
        rockOilBearingArea[name] = oilarea / rockarea
        print(name, oilarea / rockarea * 100, '%')

    # 保存数据
    f = open('BearingAreaData.csv', 'a+')
    f.write('RockNumber' + ',' + 'RockOilbearingArea\n')
    for key, value in rockOilBearingArea.items():
        data = str(key) + ',' + str(value) + '\n'
        f.write(data)
    f.close()
