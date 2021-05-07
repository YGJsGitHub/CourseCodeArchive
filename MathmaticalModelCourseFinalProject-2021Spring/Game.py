#!usr/bin/env python
# -*- coding: utf-8 -*-
# @author:ygj
# @file: 02-ClassDot.py
# @time: 2021/04/23


import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

'''
Q1:leastDotsStrategy
Q2:leastDistanceStrategy
Q3:maxSCStrategy
'''


def euclidDistance(currentPos, targetPos):
    """
    求两个位置坐标的欧式距离
    :param currentPos: 当前坐标
    :param targetPos: 目标坐标
    :return: 欧氏距离(float)
    """
    return np.sqrt(np.sum(np.square(currentPos - targetPos)))


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
        self.isArrived = False
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

    def arrived(self):
        """
        到达过的点
        """
        self.isArrived = True
        
    def backTrack(self):
        """
        搜索失败后进行回溯
        """
        self.isArrived = False


class Player:
    def __init__(self, startDot, endDot, satiety, comfort):
        """
        玩家类
        :param startDot:起点
        :param endDot:终点
        :param satiety:饱食度
        :param comfort:舒适度
        """
        self.route = [startDot, ]
        self.position = startDot.position
        self.x, self.y, self.z = self.position
        self.endDot = endDot
        self.satiety = satiety
        self.comfort = comfort

    def moveTo(self, targetDot):
        """
        移动到目标点
        :param targetDot:
        :return:
        """
        currentDot = self.route[-1]
        supply = targetDot.supply
        # 到目标点要消耗的SC(饱食度和舒适度)值
        loss = self.scCostCal(targetDot)
        # 更新饱食度和舒适度
        self.satiety = self.satiety + (not targetDot.isArrived) * targetDot.isFood * targetDot.supply - self.scCostCal(targetDot)
        self.comfort = self.comfort + (not targetDot.isArrived) * targetDot.isBonfire * targetDot.supply - self.scCostCal(targetDot)
        # 将目标点加入路径
        self.route.append(targetDot)
        # 更新玩家位置
        self.position = targetDot.position
        self.x, self.y, self.z = self.position
        # 将目标点标记为"已到达过"
        targetDot.arrived()
        # 打印移动过程
        print('From', currentDot.index, 
              'to', targetDot.index,
              currentDot.position, '--->', targetDot.position,
              'S:', self.satiety,
              'C:', self.comfort,
              'Supply:', supply,
              'Loss:', loss
              )
              
    def back(self):
        """
        回溯到上一个点
        """
        print('Back')
        currentDot = self.route[-1]
        targetDot = self.route[-2]
        # 到目标点要消耗的SC(饱食度和舒适度)值
        loss = self.__backCostCal(targetDot)
        # 更新饱食度和舒适度
        self.satiety = self.satiety - currentDot.isFood * currentDot.supply + self.__backCostCal(targetDot)
        self.comfort = self.comfort - currentDot.isBonfire * currentDot.supply + self.__backCostCal(targetDot)
        # 更新玩家位置
        self.position = targetDot.position
        self.x, self.y, self.z = self.position
        # 将当前点标记为"未到达"
        currentDot.backTrack()
        # 更新路径
        return self.route.pop()       
        
    def approachable(self, targetDot):
        """
        判断目标点是否能到达
        :param targetDot:
        :return:
        """
        scCost = self.scCostCal(targetDot)
        if (self.satiety - scCost <= -5) or (self.comfort - scCost <= -5):
            return False
        elif targetDot == self.endDot:
            if (self.satiety - scCost <= -3) or (self.comfort - scCost <= -3):
                return False
            else:
                return True
        # 保守：当目标点导致S\C下降到0以下时就放弃
        elif (self.satiety - scCost <= -5) or (self.comfort - scCost <= -5):
            return False
        else:
            return True

    def scCostCal(self, targetDot):
        """
        计算到目标点消耗的舒适度和饱食度
        :param targetDot:
        :return:
        """
        currentDot = self.route[-1]
        if self.z > targetDot.z:
            scCost = euclidDistance(currentDot.position, targetDot.position) * 4 / 100
        elif self.z < targetDot.z:
            scCost = euclidDistance(currentDot.position, targetDot.position) * 6 / 100
        else:
            scCost = euclidDistance(currentDot.position, targetDot.position) * 5 / 100
        return scCost
        
    def __backCostCal(self, targetDot):
        """
        计算回溯到目标点恢复的舒适度和饱食度
        :param targetDot:
        :return:
        """
        currentDot = self.route[-1]
        if self.z < targetDot.z:
            scCost = euclidDistance(currentDot.position, targetDot.position) * 4 / 100
        elif self.z > targetDot.z:
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
              len(self.route))

    def printRoute(self):
        """
        打印当前整条路径
        :return:
        """
        for i, dot in enumerate(self.route):
            try:
                print('Step', i, 'From:', self.route[i].index, self.route[i].position, 'to', self.route[i + 1].index,
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

def leastDotsStrategy(player, routeDots):
    """
    第一问策略：优先找最近的、补给最高的点
    """
    """
    routeDots是地图上所有可选路径点
    可用函数：
    player.moveTo(targetDot) # 移动到目标点
    player.back() # 遇到死路可以回溯
    player.approachable(targetDot) # 判断目标点是否能够到达
    player.scCostCal(targetDot) # 返回到目标点消耗的补给值
    可用属性:
    player.startDot
    player.endDot
    player.satiety
    player.comfort
    （不要更改属性值！即不要将属性作为左值赋值！）
    """
    # 计算当前可到达的位置
    approachableDots = []
    for i, dot in enumerate(routeDots):
        # 如果能到达终点
        if (dot == player.endDot) and player.approachable(player.endDot):
            player.moveTo(dot)
            return
        # 舒适度低，优先找篝火点
        if player.satiety >= player.comfort:
            if player.approachable(dot) and dot.isBonfire:
                approachableDots.append(dot)
        # 舒适度高，优先找食物点
        if player.satiety < player.comfort:
            if player.approachable(dot) and dot.isFood:
                approachableDots.append(dot)

    # 计算可到达位置里补给最多的点
    biggestDots = []
    maxValue = -float('inf')
    for i, dot in enumerate(approachableDots):
        if dot.isArrived == True:
            continue
        if dot.supply == 0:
            continue
        if dot.supply > maxValue:
            maxValue = dot.supply
    for i, dot in enumerate(approachableDots):
        if dot.isArrived == True:
            continue
        if dot.supply == maxValue:
            biggestDots.append(dot)

    targetDots = []
    for i, dot in enumerate(biggestDots):
        if dot.supply > player.scCostCal(dot) - 200:
            targetDots.append(dot)

    if len(targetDots) == 0:
        print('Died')
        return
    else:
        targetDot = targetDots[0]

    for i, dot in enumerate(biggestDots):
        if euclidDistance(dot.position, player.position) < euclidDistance(targetDot.position,
                                                                        player.position):
        # if euclidDistance(dot.position, player.endDot.position) < euclidDistance(targetDot.position,
        #                                                                        player.endDot.position):
            targetDot = dot

    player.moveTo(targetDot)
    leastDotsStrategy(player, routeDots)

def leastDistanceStrategy(player, routeDots):
    """
    第二问策略
    """
    pass

def maxSCStrategy(player, routeDots):
    """
    第三问策略
    """
    pass

    
if __name__ == "__main__":
    # Load data
    data = np.loadtxt('./data.csv', delimiter=',')
    dots = []
    for dotData in data:
        dots.append(Dot(dotData[0], dotData[1:4], dotData[4], dotData[5]))

    player1 = Player(dots[0], dots[-1], 10, 10)
    leastDotsStrategy(player1, dots)

    '''
    可视化
    '''
    # Load data
    dots = np.loadtxt('./data.csv', delimiter=',')
    routeDots = dots[1:-1, :]
    bonfireIndex = [i for i, x in enumerate(routeDots[:, 4].tolist()) if x == 0]
    foodIndex = [i for i, x in enumerate(routeDots[:, 4].tolist()) if x == 1]

    startDot = dots[0, :]  # 起点
    endDot = dots[-1, :]  # 终点
    bonfireDots = routeDots[bonfireIndex, :]  # 篝火点
    foodDots = routeDots[foodIndex, :]  # 食物点

    x, y, z = player1.getRoute()
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

    # 路径绘制
    ax.plot(x, y, z, label='route')

    # 添加坐标轴(顺序是Z, Y, X)
    ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'black'})
    ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'black'})
    ax.set_xlabel('X', fontdict={'size': 15, 'color': 'black'})
    # 添加图例
    ax.legend(loc='best')

    plt.show()
