from tkinter import *


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Node:
    def __init__(self, number, position):
        self.number = number
        self.position = position

    def __eq__(self, value):
        return self.number == value.number


class Building:
    def __init__(self, number, name, position, door, nickname, direction, size):
        self.number = number
        self.name = name
        self.position = position
        self.door = door  #node
        self.nickname = nickname  #字符串列表
        self.direction = direction #字体方向 "v"代表垂直，"h"代表水平
        self.size = size  #字体大小


class Road:
    def __init__(self, number, endpoint, degree_of_congestion, length, if_bike):
        self.number = number
        self.endpoint = endpoint  #node  路的两个端点
        self.degree_of_congestion = degree_of_congestion  #拥挤程度     （可随时间改变）
        self.length = length  #长度
        self.if_bike = if_bike  #是否能通通行自行车


class Student:
    def __init__(self, ID, position, time, start, end, start_position, end_position, strategy, which_campus):
        self.ID = ID  #""
        self.position = position
        self.time = time
        self.start = start
        self.end = end
        self.start_position = start_position
        self.end_position = end_position
        self.strategy = strategy  #导航策略
        self.which_campus = which_campus  #当前所处校区0为沙河1为海淀


class Bus:
    def __init__(self, bus_type, time, distance, time_cost):
        self.bus_type = bus_type  #车类型  0为定点班车，1为公共汽车
        self.time = time  #班车车次时间，字符串集合
        self.distance = distance
        self.time_cost = time_cost   #时间开销


class Campus:
    def __init__(self, node, road, building):
        self.node = node
        self.road = road
        self.building = building


point_size = 3
font_type = '微软雅黑'
gap = 15
adjacent_distance = 150
node_numbers = [77, 109]
road_numbers = [89, 130]
building_numbers = [42, 90]
campus = []
root = Tk()
root.geometry("400x200")  # 设置选项窗口大小
student = Student("test1", Position(45, 452.5), "2021.4.3", "", "", Position(215, 290), Position(152.5, 267.5), 1, 1)
path = []  # 路径
pass_building = []  # 途径建筑
bus_table = []  #车次表
road = []  #路径