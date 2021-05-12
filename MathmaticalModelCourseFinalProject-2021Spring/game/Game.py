#!usr/bin/env python
# -*- coding: utf-8 -*-
# @author:ygj
# @file: Game.py
# @time: 2021/04/23


import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import time

'''
Search:ygjAStar
Q1:leastDotsStrategy
Q2:leastDistanceStrategy
Q3:maxSCStrategy
'''


class Dot:
    def __init__(self, index, position, food, supply):
        """
        路径点类
        :param index: 序号
        :param position: 位置
        :param isFood: 是否为食物
        :param isBonfire: 是否为篝火
        :param isArrived: 是否到达过
        :param supply: 补给数
        :param x, y, z：坐标
        """
        self.index = int(index)
        self.position = position
        self.x, self.y, self.z = self.position
        self.isFood = bool(food)
        self.isBonfire = not bool(food)
        self.supply = supply

    def __eq__(self, other):
        """
        =运算符重载
        判断两点是否相同
        """
        return (self.index == other.index) and (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def info(self):
        """
        查看当前路径点信息
        """
        if self.isFood:
            print('Dot', self.index, ' Position: ', self.position, 'Food Supply: ', self.supply)
        elif self.isBonfire:
            print('Dot', self.index, ' Position: ', self.position, 'BonFire Supply: ', self.supply)


class Player:
    def __init__(self, startDot, endDot, satiety, comfort):
        """
        玩家类
        :param startDot:起点
        :param endDot:终点
        :param satiety:饱食度
        :param comfort:舒适度
        """
        self.route = [startDot]
        self.position = startDot.position
        self.x, self.y, self.z = self.position
        self.startDot = startDot
        self.endDot = endDot
        self.satiety, self.comfort = satiety, comfort
        self.initSC = [satiety, comfort]

    def update(self, route_set):
        '''
        更新路径信息
        :param route_set:路径
        :return:
        '''
        self.moveTo(self.startDot)
        self.route.clear()
        self.route.append(self.startDot)
        self.satiety, self.comfort = self.initSC
        for dot in route_set:
            self.moveTo(dot)

    def moveTo(self, targetDot):
        """
        移动到目标点
        :param targetDot:目标点
        :return:
        """
        currentDot = self.route[-1]
        supply = targetDot.supply
        # 到目标点要消耗的SC(饱食度和舒适度)值
        loss = self.scCostCal(targetDot)
        # 更新饱食度和舒适度
        self.satiety = self.satiety + targetDot.isFood * targetDot.supply - self.scCostCal(targetDot)
        self.comfort = self.comfort + targetDot.isBonfire * targetDot.supply - self.scCostCal(targetDot)
        # 将目标点加入路径
        self.route.append(targetDot)
        # 更新玩家位置
        self.position = targetDot.position
        self.x, self.y, self.z = self.position
        # 打印移动过程
        # print('From', currentDot.index, 
        # 'to', targetDot.index,
        # currentDot.position, '--->', targetDot.position,
        # 'S:', self.satiety,
        # 'C:', self.comfort,
        # 'Supply:', supply,
        # 'Loss:', loss
        # )

    def approachable(self, targetDot):
        """
        判断目标点是否能到达
        :param targetDot:目标点
        :return:
        """
        scCost = self.scCostCal(targetDot)
        if targetDot == self.endDot:
            return not ((self.satiety - scCost <= -3) or (self.comfort - scCost <= -3))
        else:
            return not ((self.satiety - scCost <= -5) or (self.comfort - scCost <= -5))

    def getApproachableSet(self, dots):
        """
        返回当前状态下可到达的点的list
        :param dots: 所有路径点
        :return: 可到达路径点
        """
        approachable_set = []
        for dot in dots:
            if dot in self.route:
                continue
            if player1.approachable(dot):
                approachable_set.append(dot)
        return approachable_set

    def scCostCal(self, targetDot):
        """
        计算到目标点消耗的舒适度和饱食度
        :param targetDot:目标点
        :return:消耗值
        """
        currentDot = self.route[-1]
        if self.z > targetDot.z:
            scCost = euclidDistance(currentDot.position, targetDot.position) * 4 / 100
        elif self.z < targetDot.z:
            scCost = euclidDistance(currentDot.position, targetDot.position) * 6 / 100
        else:
            scCost = euclidDistance(currentDot.position, targetDot.position) * 5 / 100
        return scCost

    def printInfo(self):
        """
        打印当前状态
        :return:
        """
        print('Position: ', self.position, 'satiety: ', self.satiety, 'comfort: ', self.comfort, 'step: ',
              len(self.route) - 1)

    def getInfo(self):
        """
        获得当前状态
        :return: 当前状态
        """
        info = 'Position: ' + str(self.position) + ' Satiety: ' + str(self.satiety) + ' Comfort: ' + str(
            self.comfort) + ' Step: ' + str(len(self.route) - 2)
        return info

    def printRoute(self):
        """
        打印当前整条路径
        :return:
        """
        for i, dot in enumerate(self.route):
            try:
                print('Step', i, ': ', self.route[i].index, '--->', self.route[i + 1].index, self.route[i].position,
                      '--->',
                      self.route[i + 1].position)
            except:
                return

    def getRoute(self):
        """
        返回玩家路径
        """
        x = []
        y = []
        z = []
        for i, dot in enumerate(self.route):
            x.append(dot.x)
            y.append(dot.y)
            z.append(dot.z)
        return x, y, z

    def getRouteLength(self):
        """
        返回路径长度
        :return:
        """
        length = 0
        for i, dot in enumerate(self.route):
            if i < len(self.route) - 1:
                length += euclidDistance(self.route[i].position, self.route[i + 1].position)
        return length


def euclidDistance(currentPos, targetPos):
    """
    求两个位置坐标的欧式距离
    :param currentPos: 当前坐标
    :param targetPos: 目标坐标
    :return: 欧氏距离(float)
    """
    return np.sqrt(np.sum(np.square(currentPos - targetPos)))


def scCostCal(startDot, targetDot):
    '''
    求两个点间的饱食度舒适度消耗
    :param startDot:起点
    :param targetDot:终点
    :return:消耗值
    '''
    if startDot.z > targetDot.z:
        scCost = euclidDistance(startDot.position, targetDot.position) * 4 / 100
    elif startDot.z < targetDot.z:
        scCost = euclidDistance(startDot.position, targetDot.position) * 6 / 100
    else:
        scCost = euclidDistance(startDot.position, targetDot.position) * 5 / 100
    return scCost


def routeVisual(searchResult):
    # 路径信息：第n条，长度l，路径点
    n, l, route = searchResult
    x, y, z = route[0], route[1], route[2]
    # Load data
    dots = np.loadtxt('./data.csv', delimiter=',')
    routeDots = dots[1:-1, :]
    bonfireIndex = [i for i, x in enumerate(routeDots[:, 4].tolist()) if x == 0]
    foodIndex = [i for i, x in enumerate(routeDots[:, 4].tolist()) if x == 1]
    startDot = dots[0, :]  # 起点
    endDot = dots[-1, :]  # 终点
    bonfireDots = routeDots[bonfireIndex, :]  # 篝火点
    foodDots = routeDots[foodIndex, :]  # 食物点
    x1, y1, z1 = bonfireDots[:, 1], bonfireDots[:, 2], bonfireDots[:, 3]
    x2, y2, z2 = foodDots[:, 1], foodDots[:, 2], foodDots[:, 3]

    # 绘图
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

    # 路径绘制
    ax.plot(x, y, z, label='route')

    # 添加坐标轴(顺序是Z, Y, X)
    ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'black'})
    ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'black'})
    ax.set_xlabel('X', fontdict={'size': 15, 'color': 'black'})
    # 添加图例
    ax.legend(loc='best')

    line = 'Number: ' + str(n) + ' Step: ' + str(len(route[0]) - 2) + ' Length: ' + str(int(round(l)))
    plt.title(line)
    # plt.show()
    savepath = str(n) + '-' + str(len(route[0]) - 2) + '-' + str(round(l)) + '.svg'
    fig.savefig(savepath, dpi=600)
    plt.close()


def leastDotsStrategy(player, approachable_set):
    """
    第一问策略：
    使[当前点到终点消耗值 - 目标点到终点消耗值 + 目标点的能量值 - 到目标点消耗的能量]尽可能大且大于0
    """
    currentDot = player.route[-1]
    endDot = player.endDot

    bestDotIndex = None
    bestDot = None
    cost = -float('inf')
    for i, dot in enumerate(approachable_set):
        if dot == player.endDot:
            bestDotIndex, bestDot = i, dot
            break
        else:
            tmp = scCostCal(currentDot, endDot) - scCostCal(dot, endDot) + dot.supply - scCostCal(currentDot, dot)
            if tmp > cost:
                bestDotIndex, bestDot = i, dot
                cost = tmp
    return bestDotIndex, bestDot


def leastDistanceStrategy(player, approachable_set):
    """
    第二问策略
    使[目标点到终点距离]尽可能小
    """
    endDot = player.endDot

    bestDotIndex = None
    bestDot = None

    cost = float('inf')

    for i, dot in enumerate(approachable_set):
        if dot == player.endDot:
            bestDotIndex, bestDot = i, dot
            break
        else:
            tmp = euclidDistance(dot.position, endDot.position)
            if tmp < cost:
                bestDotIndex, bestDot = i, dot
                cost = tmp
    return bestDotIndex, bestDot


def maxSCStrategy(player, approachable_set):
    """
    第三问策略
    """
    currentDot = player.route[-1]
    endDot = player.endDot

    bestDotIndex = None
    bestDot = None
    cost = -float('inf')
    for i, dot in enumerate(approachable_set):
        if dot == player.endDot:
            bestDotIndex, bestDot = i, dot
            break
        else:
            tmp = dot.supply - scCostCal(currentDot, dot)
            if tmp > cost:
                bestDotIndex, bestDot = i, dot
                cost = tmp
    return bestDotIndex, bestDot


def ygjAStar(player, dots, strategy, epoch=50):
    """
    改进的A*算法
    :param player: 玩家
    :param dots: 路径点
    :param strategy: 启发式策略
    :return:
    """
    def saveRoute(filename, player, time_cost, loop):
        """
        保存路径到txt文件
        :param filename:
        :param player:
        :param time_cost:
        :param loop:
        :return:
        """
        with open(filename, 'a') as f:
            f.write(player.getInfo())
            f.write(' time_cost:' + str(time_cost) + '\n')
            line = '['
            for i, dot in enumerate(player.route):
                line = line + str(dot.index) + ', '
            line = line + ']\n'
            f.write(line)
            for i, dot in enumerate(player.route):
                try:
                    line = 'Step' + str(i) + ': ' + str(player.route[i].index) + '--->' + str(
                        player.route[i + 1].index) + str(player.route[i].position) + '--->' + str(
                        player.route[i + 1].position)
                    f.write(line)
                    f.write('\n')
                except:
                    break

    time_start = time.time()
    res = 0
    minRouteLength = float('inf')

    # searchResult用于保存搜索的可行路径结果
    searchResult = []
    # 初始化open_set, route_set和approachable_set
    route_set, open_set, approachable_set = [[], [], []]
    # 将起点加入route_set中
    route_set.append(dots[0])
    # 更新当前player状态
    player.update(route_set)
    # 更新当前approachable_set，若节点在route_set中，则不加入
    approachable_set = player.getApproachableSet(dots)
    # 将approachable_set加入到open_set中
    open_set.append(approachable_set[:])
    # 如果open_set不为空
    while open_set:
        # 如果open_set[-1]不为空
        if open_set[-1]:
            # 从open_set[-1]中根据*启发式*选取优先级最高的点n:
            i, bestDot = strategy(player, open_set[-1][:])
            # 如果节点为终点
            if bestDot == player.endDot:
                res += 1
                print(res)
                # 将节点n从open_set[-1]中删除(open_set[-1].pop())，并加入route_set中
                route_set.append(open_set[-1].pop(i))
                # 更新当前player状态
                player.update(route_set)
                # 记录route_set(不小于历史最优的路径不予以保存)
                if True:
                    minRouteLength = len(route_set) - 1
                    time_end = time.time()
                    time_cost = time_end - time_start
                    filename = './route/' + str(res) + '-' + str(len(route_set) - 1) + '.txt'
                    saveRoute(filename, player1, time_cost, res)
                    searchResult.append([res, player.getRouteLength(), player.getRoute()])
                if res <= epoch:  # 50次搜索
                    # 进行下一次搜索
                    route_set.pop()
                    player.update(route_set)
                    continue
                else:
                    return searchResult
            # 如果节点n不是终点
            else:
                # 将节点n从open_set[-1]中删除(open_set[-1].pop())，并加入route_set中
                route_set.append(open_set[-1].pop(i))
                # 更新当前player状态
                player.update(route_set)
                # 更新当前approachable_set，若节点在route_set中，则不加入
                approachable_set.clear()
                approachable_set = player.getApproachableSet(dots)
                # 将approachable_set加入到open_set中
                open_set.append(approachable_set[:])
        # 如果open_set[-1]为空
        else:
            # print('back!')
            open_set.pop()
            route_set.pop()
            player.update(route_set)
        # 显示部分
        # i = os.system("cls")
        # print('-----------------------------')
        # print(len(open_set))
        # player.printInfo()
        # print(len(player.getApproachableSet(dots)))
        # player.printRoute()
        # print('-----------------------------')


if __name__ == "__main__":
    # Load data
    data = np.loadtxt('./data.csv', delimiter=',')
    dots = []
    for dotData in data:
        dots.append(Dot(dotData[0], dotData[1:4], dotData[4], dotData[5]))
    # Init player
    player1 = Player(dots[0], dots[-1], 10, 10)
    # A* Search
    searchResults = ygjAStar(player1, dots, maxSCStrategy, epoch=500)
    # Visualiation
    for searchResult in searchResults:
        routeVisual(searchResult)