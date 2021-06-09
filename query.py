from tkinter import *
from data import *
import output as out
import navigate

def query():
    print("in query")
    root_query = Tk()
    root_query.geometry("400x200")  # 设置窗口大小

    #location_button = Button(root_query, text="查询所处位置", command=lambda:location(root))
    #building_around_button = Button(root_query, text="查询周围建筑及其最短距离", command=building_around)
    #location_button.pack()
    #building_around_button.pack()
    root_query.mainloop()
    return

def location(map_root, canvas):
    out.paint_point(canvas, student.position.x + gap, student.position.y + gap, color='#FFFF00')
    global  switch
    switch = 1
#    return
def building_around_button(map_root, canvas):
    global switch
    switch = 1
    #生成出如口列表
    door = []
    near_building = []
    temp = []
    for i in range(building_numbers[student.which_campus]+1):
        door.extend(campus[student.which_campus].building[i].door)
    #去重复
    for i in door.copy():
        if door.count(i) > 1:
            door.remove(i)
    #去除直线距离超出的出入口
    for i in door.copy():
        if ((student.position.x-i.position.x)**2+(student.position.y-i.position.y)**2) > adjacent_distance**2:
            door.remove(i)
    #去除直线距离超出的出入口
    for i in door.copy():
        path.clear()
        student.start_position = student.position
        student.end_position = i.position
        navigate.shortest_path_incampus_method1(student.strategy)
        if calculate_shotest_distance() > adjacent_distance:
            door.remove(i)
    #将出入口对应建筑以及位置信息分析提取出
    for i in range(len(door)):
        for j in range(building_numbers[student.which_campus] + 1):
            if campus[student.which_campus].building[j].door.count(door[i]) > 0:
                near_building.append([campus[student.which_campus].building[j].name, campus[student.which_campus].building[j].position, door[i]])
    #除去重复建筑物
    for i in near_building:
        count = 0
        for j in temp:
            if i[0] == j[0]:
                count += 1
        if count == 0:
            temp.append(i)
    near_building = temp
    #跳转模拟导航触发函数
    def to_navigate(index):
        path.clear()
        student.start_position = student.position
        student.end_position = near_building[index][2].position
        navigate.shortest_path_incampus_method1()
        map_root.destroy()
        navigate.navigator_one_campus()
    #生成可点击文本组件
    for index, building in enumerate(near_building):
        Button(map_root, text=building[0], foreground='#FF0000', command=lambda idx=index: to_navigate(idx)).place(x=building[1].x + 300, y=building[1].y + gap, anchor='center')
    canvas.pack()
    map_root.mainloop()
    return

def building_around():
    map_root = Tk()
    map_root.geometry("1000x600")  # 设置地图窗口大小
    canvas = Canvas(map_root, bg='white')
    canvas.config(width=400 + 2 * gap, height=575 + 2 * gap)  # 画布大小
    out.fill_campus_canvas(canvas, campus[student.which_campus])

    #生成出如口列表
    door = []
    near_building = []
    temp = []
    for i in range(building_numbers[student.which_campus]+1):
        door.extend(campus[student.which_campus].building[i].door)
    #去重复
    for i in door.copy():
        if door.count(i) > 1:
            door.remove(i)
    #去除直线距离超出的出入口
    for i in door.copy():
        if ((student.position.x-i.position.x)**2+(student.position.y-i.position.y)**2) > adjacent_distance**2:
            door.remove(i)
    #去除直线距离超出的出入口
    for i in door.copy():
        path.clear()
        student.start_position = student.position
        student.end_position = i.position
        navigate.shortest_path_incampus_method1(student.strategy)
        if calculate_shotest_distance() > adjacent_distance:
            door.remove(i)
    #将出入口对应建筑以及位置信息分析提取出
    for i in range(len(door)):
        for j in range(building_numbers[student.which_campus] + 1):
            if campus[student.which_campus].building[j].door.count(door[i]) > 0:
                near_building.append([campus[student.which_campus].building[j].name, campus[student.which_campus].building[j].position, door[i]])
    #除去重复建筑物
    for i in near_building:
        count = 0
        for j in temp:
            if i[0] == j[0]:
                count += 1
        if count == 0:
            temp.append(i)
    near_building = temp
    #跳转模拟导航触发函数
    def to_navigate(index):
        path.clear()
        student.start_position = student.position
        student.end_position = near_building[index][2].position
        navigate.shortest_path_incampus_method1()
        map_root.destroy()
        navigate.navigator_one_campus()
    #生成可点击文本组件
    for index, building in enumerate(near_building):
        Button(map_root, text=building[0], foreground='#FF0000', command=lambda idx=index: to_navigate(idx)).place(x=building[1].x + 300, y=building[1].y + gap, anchor='center')
    canvas.pack()
    map_root.mainloop()
    return

def calculate_shotest_distance():
    i = 0
    distance = 0
    for node2 in path:
        if i == 0:
            node1 = path[0]
        else:
            node1 = path[i-1]
        i += 1
        if node1.position.x == node2.position.x:
            distance += abs(node1.position.y - node2.position.y)
        elif node1.position.y == node2.position.y:
            distance += abs(node1.position.x - node2.position.x)
    return distance
