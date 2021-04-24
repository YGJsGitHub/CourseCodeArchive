# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# author:ygj time:2021/3/29


import cv2 as cv
import glob
import re
import os


# 裁剪单张图片
def imgCrop(imgpath, width, length):
    img = cv.imread(imgpath)
    cnt = 1
    for w in range(0, img.shape[0], width):
        for l in range(0, img.shape[1], length):
            if ((w + width) > img.shape[0]) | ((l + length) > img.shape[1]):
                print('Overflow')
                break
            cropped = img[w:w + width, l:l + length]
            print(imgpath + '' + str(cnt))

            savepath = savePath(imgpath, cnt)
            cv.imwrite(savepath, cropped)
            cnt += 1
        break
    os.remove(imgpath)


# 获取保存路径
def savePath(imgpath, cnt):
    pattern = r'.*[0-9]'
    mat = re.match(pattern, imgpath, flags=0)
    savepath = mat.group(0) + '-' + str(cnt) + imgpath.replace(mat.group(0), '')
    return savepath


# 裁剪文件夹下所有图片
def cropImg(imgpaths, width, length):
    for imgpath in glob.glob(imgpaths):
        print(imgpath)
        imgCrop(imgpath, width, length)


'''
在这里更改你的设置，包括目录、图片类别和裁剪大小
'''
# rootpath是目标图片的根目录，不能包含中文
rootpath = r".\stone\*"
# imgpaths的数字1和2选择岩石图像或是荧光图像 1是岩石 2是荧光
imgpaths = rootpath + "\*-1.*"
# width和length为你需要裁剪到的图片的宽和高
width = 500
length = 600

if __name__ == "__main__":
    cropImg(imgpaths, width, length)
