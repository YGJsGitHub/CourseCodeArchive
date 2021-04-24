#!usr/bin/env python
# -*- coding: utf-8 -*-
# @author:ygj
# @file: 00-All.py
# @time: 2021/04/24


import numpy as np


'''
Todolist:
1. 读取xlsx √
2. 三维图绘制: 两种点(rgb索引) 大小(s=int) √
3. python Queue
4. 函数：3维图动态更新:多点之间划线，输出gif
5. 函数：当前点可到达范围
6. 搜索策略：如何同时考虑两个指标
    Q1:只走补给数量最高的点，且尽可能离终点近
    Q2:只走尽可能离终点近的点
    Q3:
7. 可选优化：实用3B1B语言实现动画
8. 如何记忆路线上的点，更新吃过的点为0
    -维护一个已到达点的列表，每次检查
'''