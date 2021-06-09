from data import *
import data
from tkinter import *
import math
import output as out
import tkinter.messagebox
import query
import copy
import datetime
import time

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
    radio4 = Radiobutton(root_navigator, text="策略四", variable=radio, value=4)
    radio4.grid(row=2, column=3)

    def submit():
        student.start = e_start.get()
        student.end = e_end.get()
        student.strategy = radio.get()
        root_navigator.destroy()
        if student.strategy in [1, 2, 3]:
            navigator_mode()
        elif student.strategy == 4:
            input_pass_building()

    b_submit = Button(root_navigator, text='确定', command=submit)
    b_submit.grid(row=3, sticky=E)
    root_navigator.mainloop()
    return

#def change_navigate():

def navigator_mode():
    start = search_point(student.start)
    end = search_point(student.end)
    temp_list = []
    #root_start = Tk()
    #root_end = Tk()
    #判断输入点是否存在
    if (start[1] == -1) or (end[1] == -1):
        root_alarm = Tk()
        root_alarm.geometry("400x200")
        word = Message(root_alarm, text="输入无效\n请查询地图后重新输入", font=('Helvetica', '15'))
        word.pack()
        root_alarm.mainloop()
        return

    if (start[1] == -2):
        root_start = Tk()
        root_start.geometry("400x200")
        word = Message(root_start, text="起点校区建筑重名\n请选择校区", font=('Helvetica', '10'))
        word.pack()
        haidian_button = Button(root_start, text="海淀", command=lambda:duplicate_button(root_start, "海淀", student.start, temp_list))
        shahe_button = Button(root_start, text="沙河", command=lambda:duplicate_button(root_start, "沙河", student.start, temp_list))
        start = temp_list
        haidian_button.pack()
        shahe_button.pack()
        root_start.mainloop()
        print("sadddddddddddddd")

    if (end[1] == -2):
        root_end = Tk()
        root_end.geometry("400x200")
        word = Message(root_end, text="终点校区建筑重名\n请选择校区", font=('Helvetica', '10'))
        word.pack()
        haidian_button = Button(root_end, text="海淀", command=lambda:duplicate_button(root_end, "海淀", student.end, temp_list))
        shahe_button = Button(root_end, text="沙河", command=lambda:duplicate_button(root_end, "沙河", student.end, temp_list))
        end = temp_list
        
        haidian_button.pack()
        shahe_button.pack()
        root_end.mainloop()
        print("sadddddddddddddd")

    student.start_position = start[0].position
    student.end_position = end[0].position

    if start[1] == end[1]:
        print("起点终点在同一校区内")
        student.which_campus = int(start[1])
        navigator_one_campus()
    else:
        print("起点终点在不同校区内")
        #输入校区间乘坐交通工具的选择
        root_navigator = Tk()
        root_navigator.geometry("400x200")
        radio = IntVar(root_navigator)
        radio.set(0)
        radio1 = Radiobutton(root_navigator, text="定点班车", variable=radio, value=0)
        radio1.grid(row=0, column=0)
        radio2 = Radiobutton(root_navigator, text="公共汽车", variable=radio, value=1)
        radio2.grid(row=0, column=1)

        def submit():
            bus_choice = radio.get()
            root_navigator.destroy()
            navigator_two_campus(bus_choice, start[1], end[1])

        b_submit = Button(root_navigator, text='确定', command=submit)
        b_submit.grid(row=0, column=2)
        root_navigator.mainloop()
    #root_start.mainloop()
    #root_end.mainloop()

def duplicate_button(root, text, end_or_start, temp_list):
    if text == "海淀":
        for element in campus[1].building:
            if end_or_start == element.name or end_or_start in element.nickname:
                temp_list.append(element.door[0])
                temp_list.append(1)
    else:
        for element in campus[0].building:
            if end_or_start == element.name or end_or_start in element.nickname:
                temp_list.append(element.door[0])
                temp_list.append(0)
    root.destroy()
    return

def navigator_one_campus():
    print(student.start)
    print(student.start_position)
    print(student.end)
    print(student.end_position)
    print(student.strategy)

    if student.strategy in [1, 2, 3]:
        shortest_path_incampus_method1(student.strategy)
    elif student.strategy == 4:
        shortest_passing_by()

    for j in range(len(path) - 1):
        for road_pass in campus[student.which_campus].road:
            if (path[j] in road_pass.endpoint) and (path[j + 1] in road_pass.endpoint):
                road.append(road_pass)
                break

    out.imaging_path(campus[student.which_campus], path, road)

    return

def navigator_two_campus(bus_choice, start_campus, end_campus):
    #第一地点的输入处理（海淀区到东门，沙河校区到西门）
    #东门Node(42, Position(400, 225))
    #西门Node(1, Position(0, 130))
    end_position = Position(student.end_position.x, student.end_position.y)
    if start_campus == 0:
        student.end = "西门"
        student.end_position = Position(0, 130)
    elif start_campus == 1:
        student.end = "东门"
        student.end_position = Position(400, 225)
    # 校区内导航
    path.clear()
    student.which_campus = start_campus
    navigator_one_campus()
    #校区间导航
    between_campus_simulate(bus_choice)
    # 第二地点的输入处理（海淀区到东门，沙河校区到西门）
    student.end_position = end_position
    if end_campus == 0:
        student.start = "西门"
        student.start_position = Position(0, 130)
    elif end_campus == 1:
        student.start = "东门"
        student.start_position = Position(400, 225)
    # 校区内导航
    path.clear()
    student.which_campus = end_campus
    navigator_one_campus()
    return

def search_point(s):#返回入口与一个校区
    list = []
    #检测是否为两校区共有地点
    judge = 0

    for element in campus[0].building:
        if s == element.name or s in element.nickname:
            judge = 1
            break
    for element in campus[1].building:
        if s == element.name or s in element.nickname:
            judge = 0
            break
        else:
            judge = 1

    if judge == 0:
        print("出现重名")
        list.append(Position(-1, -1))
        list.append(-2)
        return list
    else:
        print("未出现重名")
    #遍历沙河
    for element in campus[0].building:
        if s == element.name or s in element.nickname:
            list.append(element.door[0])
            list.append(0)
            return list
    #遍历海淀
    for element in campus[1].building:
        if s == element.name or s in element.nickname:
            list.append(element.door[0])
            list.append(1)
            return list

    print("起点或终点输入无效，请重新输入")
    list.append(Position(-1, -1))
    list.append(-1)
    return list

def input_pass_building():
    root_input_pass = Tk()
    root_input_pass.geometry("400x200")
    l_input_pass = Label(root_input_pass, text='途径地点：')
    l_input_pass.grid(row=0, sticky=W)
    e_input_pass = Entry(root_input_pass)
    e_input_pass.grid(row=0, column=1, sticky=E)

    def add_pass():
        pass_building.append(e_input_pass.get())
        tkinter.messagebox.askokcancel(title='添加', message='添加成功！')

    b_add_pass = Button(root_input_pass, text='添加', command=add_pass)
    b_add_pass.grid(row=0, column=2)

    def jump_to_navigate():
        root_input_pass.destroy()
        navigator_one_campus()

    b_jump = Button(root_input_pass, text='确定', command=jump_to_navigate)
    b_jump.grid(row=0, column=3)
    return

def between_campus_simulate(bus_choice):
    idx = 0
    for i in bus_table[bus_choice].time:
        if i > student.time:
            break
        else:
            idx += 1
    wait_time = str(bus_table[bus_choice].time[idx]-student.time)
    #等待状态(包含等车和在车上的时间)
    time_count(wait_time, "车已到站!", bus_table[bus_choice].time_cost)
    #改变student的时间

    tkinter.messagebox.showwarning('等待中...', '请在车到站后点击确定')
    return

def to_s(t):
    h, m, s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

def time_count(delta_time, show_msg, time_cost):
    print(delta_time)
    root_navigator_tmp = Tk()
    root_navigator_tmp.title("倒计时")
    root_navigator_tmp.geometry("400x200")
    time_sec = to_s(delta_time)
    all_time = Label(root_navigator_tmp, text='总计时间：'+str(delta_time))
    all_time.grid(row=0, column=0)

    def foo(times):
        times = times - 1
        clock = but.after(1000, foo, times)
        if times == 0:
            but.after_cancel(clock)
            tkinter.messagebox.askokcancel(title='到达', message=show_msg)
            if time_cost != 0:
                minute, second = (time_cost // 60, time_cost % 60)
                hour = 0
                if minute > 60:
                    hour, minute = (minute // 60, minute % 60)
                root_navigator_tmp.destroy()
                time_count(str(hour) + ":" + str(minute) + ":" + str(second), "车已到达校区", 0)
                return
            root_navigator_tmp.destroy()
            return
        else:
            minute, second = (times // 60, times % 60)
            hour = 0
            if minute > 60:
                hour, minute = (minute // 60, minute % 60)
            but["text"] = '剩余时间：'+str(hour)+":"+str(minute)+":"+str(second)
    but = Button(root_navigator_tmp, text="", width=20)
    but.grid(row=1, column=0)
    foo(time_sec)
    return

def shortest_path_incampus_method1(method):#传参数 method
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
            if  (road.endpoint[0].position.x-node_start.position.x)*(road.endpoint[1].position.x-node_start.position.x)<=0.001 and (road.endpoint[0].position.y-node_start.position.y)*(road.endpoint[1].position.y-node_start.position.y)<=0.001 and math.isclose((road.endpoint[0].position.y-node_start.position.y)*(node_start.position.x-road.endpoint[1].position.x), (node_start.position.y-road.endpoint[1].position.y)*(road.endpoint[0].position.x-node_start.position.x), rel_tol=0.001):
                road_store = road
                campus[student.which_campus].road.append(Road(131, [road.endpoint[0], node_start], road.degree_of_congestion , ((road.endpoint[0].position.x - node_start.position.x) ** 2 + (road.endpoint[0].position.y - node_start.position.y) ** 2) ** 0.5, road.if_bike))
                campus[student.which_campus].road.append(Road(132, [road.endpoint[1], node_start], road.degree_of_congestion , ((road.endpoint[1].position.x - node_start.position.x) ** 2 + (road.endpoint[1].position.y - node_start.position.y) ** 2) ** 0.5, road.if_bike))
                campus[student.which_campus].road.remove(road)
                break
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

def shortest_passing_by():
    pass_node = []
    start_head = student.start_position
    start_tail = student.end_position
    pass_node_test = []
    pass_node_dis = []
    distance = []
    path_get_frhead = []
    path_get_frtail = []
    for s in pass_building:
        pass_node.append(search_point(s)[0])
    while pass_node != []:
        student.start_position = start_head
        for node in pass_node:
            student.end_position = node.position
            data.path.clear()
            shortest_path_incampus_method1(1)
            distance.append(query.calculate_shotest_distance())#[d1 d2 ...]
            pass_node_test.append(node)
            pass_node_dis.append(copy.deepcopy(path)) #[[][]...[p1 p2...]]
        index = distance.index(min(distance))
        path_get_frhead.extend(pass_node_dis[index])
        start_head = pass_node_test[index].position
        path_get_frhead.pop()
        pass_node.remove(pass_node_test[index])
        distance.clear();pass_node_dis.clear();pass_node_test.clear()

        if pass_node != []:
            student.start_position = start_tail
            for node in pass_node:
                student.end_position = node.position
                data.path.clear()
                shortest_path_incampus_method1(1)
                distance.append(query.calculate_shotest_distance())  # [d1 d2 ...]
                pass_node_test.append(node)
                pass_node_dis.append(copy.deepcopy(path))  # [[][]...[p1 p2...]]
            index = distance.index(min(distance))
            path_get_frtail.extend(pass_node_dis[index])
            start_tail = pass_node_test[index].position
            path_get_frtail.pop()
            pass_node.remove(pass_node_test[index])
            distance.clear();pass_node_dis.clear();pass_node_test.clear()
    student.start_position = start_head
    student.end_position = start_tail
    data.path.clear()
    shortest_path_incampus_method1(1)
    path_get_frhead.extend(path)
    path_get_frtail.reverse()
    path_get_frhead.extend(path_get_frtail)
    data.path.clear()
    data.path.extend(path_get_frhead)
