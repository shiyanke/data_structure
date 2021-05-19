from data import *
import data
from tkinter import *
import math
import output as out


def navigate():
    print("in navigate")
    root_navigator = Tk()
    root_navigator.geometry("400x200")
    l_start = Label(root_navigator, text='起点：')
    l_start.grid(row=0, sticky=W)
    e_start = Entry(root_navigator)
    e_start.grid(row=0, column=1, sticky=E)

    l_end = Label(root_navigator, text='终点：')
    l_end.grid(row=1, sticky=W)
    e_end = Entry(root_navigator)
    e_end.grid(row=1, column=1, sticky=E)

    radio = IntVar(root_navigator)
    radio.set(1)
    radio1 = Radiobutton(root_navigator, text="策略一", variable=radio, value=1)
    radio1.grid(row=2, column=0)
    radio2 = Radiobutton(root_navigator, text="策略二", variable=radio, value=2)
    radio2.grid(row=2, column=1)
    radio3 = Radiobutton(root_navigator, text="策略三", variable=radio, value=3)
    radio3.grid(row=2, column=2)

    def submit():
        student.start = e_start.get()
        student.end = e_end.get()
        student.strategy = radio.get()
        root_navigator.destroy()
        navigator_one_campus()
    b_submit = Button(root_navigator, text='确定', command=submit)
    b_submit.grid(row=2, column=3)
    root_navigator.mainloop()
    return


def navigator_mode():
    '''
    校区内return一种值
    校区间return一种值
    '''


def navigator_one_campus():
    print(student.start)
    print(student.end)
    print(student.strategy)
    out.imaging(campus[1])
    return


def navigator_two_campus():
    return


def shortest_path_incampus_method1():#传参数 method
    method = 2
    '''传参数1.最短路径 2.最短时间 3.最短自行车时间'''
    node_end = Node(0, Position(0, 0))
    node_start = Node(0, Position(0, 0))
    flag = 0
    node_number = node_numbers[student.which_campus]
    for node in campus[student.which_campus].node:
        if node.position.x == student.end_position.x and node.position.y == student.end_position.y:
            node_end = node
    for node in campus[student.which_campus].node:
        if node.position.x == student.start_position.x and node.position.y == student.start_position.y:
            node_start = node
            flag = 1
            break
    if flag == 0:
        campus[student.which_campus].node.append(Node(node_number + 1, student.start_position))
        node_start = campus[student.which_campus].node[node_number + 1]#起始点，终止点
        road_store = Road(-1, [Position(0, 0), Position(0, 0)], 0, 0, 0)
        for road in campus[student.which_campus].road:
            if ((road.endpoint[0].position.x == node_start.position.x and road.endpoint[1].position.x == node_start.position.x) and \
                ((road.endpoint[0].position.y > node_start.position.y and node_start.position.y > road.endpoint[1].position.y) or\
                 (road.endpoint[0].position.y < node_start.position.y and node_start.position.y <road.endpoint[1].position.y))) or \
                    ((road.endpoint[0].position.y == node_start.position.y and road.endpoint[1].position.y == node_start.position.y) and\
                     ((road.endpoint[0].position.x > node_start.position.x and node_start.position.x > road.endpoint[1].position.x)or\
                      (road.endpoint[0].position.x < node_start.position.x and node_start.position.x < road.endpoint[1].position.x))):
                road_store = road
                campus[student.which_campus].road.append(Road(131, [road.endpoint[0], node_start], road.degree_of_congestion \
                                                              , ((road.endpoint[0].position.x - node_start.position.x) ** 2 \
                                                                + (road.endpoint[0].position.y - node_start.position.y) ** 2) ** 0.5, road.if_bike))
                campus[student.which_campus].road.append(Road(132, [road.endpoint[1], node_start], road.degree_of_congestion \
                                                              , ((road.endpoint[1].position.x - node_start.position.x) ** 2 \
                                                                + (road.endpoint[1].position.y - node_start.position.y) ** 2) ** 0.5, road.if_bike))
                campus[student.which_campus].road.remove(road)
        node_number += 1
    dist = []#存距离
    path_get = []#前一个表存点，后一个表存路
    adj_list = []#存每个点的邻接点
    pre_path = []#路径列表
    temp_path = []
    adj_dis = []
    adj_weight = []
    '''构建邻接表'''
    '''初始化邻接表与前缀路径表'''
    i = 0
    while (i <= node_number):
        adj_list.append([])
        pre_path.append([])
        adj_dis.append([])
        adj_weight.append([])
        i += 1
    '''填充邻接表'''
    for road in campus[student.which_campus].road:
        if road.endpoint[1] not in adj_list[road.endpoint[0].number]:
            if(method == 3):
                if(road.if_bike == 1):
                    adj_list[road.endpoint[0].number].append(road.endpoint[1])
                    adj_dis[road.endpoint[0].number].append(road.length)
                    adj_weight[road.endpoint[0].number].append(road.degree_of_congestion)
            else:
                adj_list[road.endpoint[0].number].append(road.endpoint[1])
                adj_dis[road.endpoint[0].number].append(road.length)
                if (method != 1):
                    adj_weight[road.endpoint[0].number].append(road.degree_of_congestion)
                else:
                    adj_weight[road.endpoint[0].number].append(1)
        if road.endpoint[0] not in adj_list[road.endpoint[1].number]:
            if(method == 3):
                if(road.if_bike == 1):
                    adj_list[road.endpoint[1].number].append(road.endpoint[0])
                    adj_dis[road.endpoint[1].number].append(road.length)
                    adj_weight[road.endpoint[1].number].append(road.degree_of_congestion)
            else:
                adj_list[road.endpoint[1].number].append(road.endpoint[0])
                adj_dis[road.endpoint[1].number].append(road.length)
                if (method != 1):
                    adj_weight[road.endpoint[1].number].append(road.degree_of_congestion)
                else:
                    adj_weight[road.endpoint[1].number].append(1)

    '''初始化dist'''
    i = 0
    while i <= node_number:
        dist.append(999.9)
        i = i+1
    dist[node_start.number] = 0
    status = 0
    '''选取最小距离，加入path_get'''
    while 1:
        if node_end not in path_get:
            min = 999.9
            min_index = 0
            j = 0
            while j <= node_number:
                if dist[j] < min and campus[student.which_campus].node[j] not in path_get:
                    min = dist[j]
                    min_index = j
                j +=1
            path_get.append(campus[student.which_campus].node[min_index])
            '''找到新加入点的前缀点，方便做路径跟踪'''
            for node in path_get:
                if node in adj_list[min_index]:
                    posi = adj_list[min_index].index(node)
                    dis = adj_dis[min_index][posi] / adj_weight[min_index][posi]
                    if math.isclose(dist[node.number] + dis , dist[min_index],rel_tol=0.001):
                        pre_path[min_index].append(node)
            '''改变dist列表'''
            for element in adj_list[min_index]:
                if element not in path_get:
                    posi = adj_list[min_index].index(element)
                    bi_dist = adj_dis[min_index][posi] / adj_weight[min_index][posi]
                    if dist[element.number] > dist[min_index] + bi_dist:
                        dist[element.number] = dist[min_index] + bi_dist
            if (path_get.count(campus[student.which_campus].node[0]) > 1):
                status = 1
                break
        else :
            break
    '''将路径跟踪的结果放在new_path里'''
    if(status != 1):
        index = node_end.number
        while node_start not in data.path :
            data.path.append(pre_path[index][0])
            index = pre_path[index][0].number
        '''倒叙输入path,加上终点'''
        temp_path.extend(path)
        path.clear()
        path.extend(list(reversed(temp_path)))
        path.append(node_end)
        if flag == 0:
            campus[student.which_campus].road.pop()
            campus[student.which_campus].road.pop()
            campus[student.which_campus].road.append(road_store)
        campus[student.which_campus].node.pop()
    else:
        path.clear()
    return


