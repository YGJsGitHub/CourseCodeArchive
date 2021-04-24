# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# author:ygj time:2021/3/31


import cv2
import numpy as np
import glob


# Trackbar callback function
def callback(object):
    pass


# 选择HSV阈值
def Choose_Color(img):
    img = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))

    cv2.imshow("image", img)

    cv2.createTrackbar("H_min", "image", 0, 255, callback)
    cv2.createTrackbar("H_max", "image", 77, 255, callback)

    cv2.createTrackbar("S_min", "image", 43, 255, callback)
    cv2.createTrackbar("S_max", "image", 255, 255, callback)

    cv2.createTrackbar("V_min", "image", 46, 255, callback)
    cv2.createTrackbar("V_max", "image", 255, 255, callback)

    while (True):

        H_min = cv2.getTrackbarPos("H_min", "image", )
        S_min = cv2.getTrackbarPos("S_min", "image", )
        V_min = cv2.getTrackbarPos("V_min", "image", )

        H_max = cv2.getTrackbarPos("H_max", "image", )
        S_max = cv2.getTrackbarPos("S_max", "image", )
        V_max = cv2.getTrackbarPos("V_max", "image", )

        lower_hsv = np.array([H_min, S_min, V_min])
        upper_hsv = np.array([H_max, S_max, V_max])

        mask = cv2.inRange(img, lower_hsv, upper_hsv)

        # print("H_min = %d,H_max = %d,S_min = %d,S_max = %d,V_min = %d,V_max = %d"%(H_min,H_max,S_min,S_max,V_min,V_max))

        cv2.imshow("mask", mask)

        if cv2.waitKey(1) & 0XFF == 27:
            break

# 数据读取
rootpath = r".\b_data\rock_data"
imgpaths = rootpath + "\*-2.*"

if __name__ == "__main__":
    for imgpath in glob.glob(imgpaths):
        print(imgpath)
        testpath = r'.\b_data\test\126-2.bmp'
        img = cv2.imread(imgpath, cv2.COLOR_RGB2HSV)
        Choose_Color(img)
