#!usr/bin/env python
# -*- coding: utf-8 -*-
# @author:ygj
# @file: 01-dataVisuliation.py
# @time: 2021/04/23


import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":
    # Load data
    dots = np.loadtxt('./data.csv', delimiter=',')
    routeDots = dots[1:-1, :]
    bonfireIndex = [i for i, x in enumerate(routeDots[:, 4].tolist()) if x == 0]
    foodIndex = [i for i, x in enumerate(routeDots[:, 4].tolist()) if x == 1]

    startDot = dots[0, :]  # 起点
    endDot = dots[-1, :]  # 终点
    bonfireDots = routeDots[bonfireIndex, :]  # 篝火点
    foodDots = routeDots[foodIndex, :]  # 食物点

    '''
    可视化
    '''
    x1, y1, z1 = bonfireDots[:, 1], bonfireDots[:, 2], bonfireDots[:, 3]
    x2, y2, z2 = foodDots[:, 1], foodDots[:, 2], foodDots[:, 3]

    fig = plt.figure()
    ax = Axes3D(fig)
    # 图例设置
    startMarker = '$\circledS$'
    endMarker = '$\circledE$'

    # 散点绘制
    ax.scatter(startDot[1], startDot[2], startDot[3], c='b', s=200, marker=startMarker, label='start')
    ax.scatter(endDot[1], endDot[2], endDot[3], c='b', s=200, marker=endMarker, label='end')
    ax.scatter(x1, y1, z1, c='#FFA500', s=np.exp2(bonfireDots[:, 5]) * 6, marker='^', label='bonfireDot')
    ax.scatter(x2, y2, z2, c='#68DE69', s=np.exp2(foodDots[:, 5]) * 3, label='foodDot')

    # 添加坐标轴(顺序是Z, Y, X)
    ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'black'})
    ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'black'})
    ax.set_xlabel('X', fontdict={'size': 15, 'color': 'black'})
    # 添加图例
    ax.legend(loc='best')

    plt.show()
    # fig.savefig('scatter.svg', dpi=600, format='eps')
