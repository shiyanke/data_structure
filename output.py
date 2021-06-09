from data import *
from tkinter import *
import time
import query
import navigate

def view_campus():
    print("in view_campus")
    root_view = Tk()
    root_view.geometry("400x200")
    shahe_button = Button(root_view, text="沙河地图", command=lambda:imaging(campus[0]))
    haidian_button = Button(root_view, text="海淀地图", command=lambda:imaging(campus[1]))
    shahe_button.pack()
    haidian_button.pack()
    root_view.mainloop()
    return

def paint_point(cv, x, y, color="#0000FF"):  #蓝色
    x1, y1 = (x - point_size), (y - point_size)
    x2, y2 = (x + point_size), (y + point_size)
    cv.create_oval(x1, y1, x2, y2, fill=color)

def fill_campus_canvas(canvas, one_campus):
    #节点（出入口、路口）、路、建筑物
    points = one_campus.node
    roads = one_campus.road
    buildings = one_campus.building
    for j in points:
        paint_point(canvas, j.position.x + gap, j.position.y + gap)
    for j in roads:
        canvas.create_line(j.endpoint[0].position.x + gap, j.endpoint[0].position.y + gap, j.endpoint[1].position.x + gap, j.endpoint[1].position.y + gap, fill="#808080")
    for j in buildings:
        if j.direction == "v":
            canvas.create_text((j.position.x + gap, j.position.y + gap), font=(font_type, j.size), text="\n".join(j.name), fill="#000000", anchor='center')
        elif j.direction == "h":
            canvas.create_text((j.position.x + gap, j.position.y + gap), font=(font_type, j.size), text=j.name, fill="#000000", anchor='center')
    return
#校区临时绘图
def imaging(one_campus):
    map_root = Tk()
    map_root.geometry("1000x600")  # 设置地图窗口大小
    canvas = Canvas(map_root, bg='white')
    canvas.config(width=600 + 2 * gap, height=600 + 2 * gap)  # 画布大小
    #节点（出入口、路口）、路、建筑物
    points = one_campus.node
    roads = one_campus.road
    buildings = one_campus.building
    for j in points:
        paint_point(canvas, j.position.x + gap, j.position.y + gap)
    for j in roads:
        canvas.create_line(j.endpoint[0].position.x + gap, j.endpoint[0].position.y + gap, j.endpoint[1].position.x + gap, j.endpoint[1].position.y + gap, fill="#808080")
    for j in buildings:
        if j.direction == "v":
            canvas.create_text((j.position.x + gap, j.position.y + gap), font=(font_type, j.size), text="\n".join(j.name), fill="#000000", anchor='center')
        elif j.direction == "h":
            canvas.create_text((j.position.x + gap, j.position.y + gap), font=(font_type, j.size), text=j.name, fill="#000000", anchor='center')
    canvas.pack()
    map_root.mainloop()
    return
#绘制路线
def imaging_path(one_campus, path, road):
    student.query_time = time.localtime(time.time())
    student.need_time = 0
    map_root = Tk()
    map_root.geometry("1000x1000")  # 设置地图窗口大小
    #location_button = Button(map_root, text="查询所处位置", command=lambda:query.location(map_root))
    #change_button = Button(map_root, text="更改导航策略", command=navigate.change_navigate)
    canvas = Canvas(map_root, bg='white')
    canvas.config(width=600 + 2 * gap, height=600 + 2 * gap)  # 画布大小
    #节点（出入口、路口）、路、建筑物
    points = one_campus.node
    roads = one_campus.road
    buildings = one_campus.building
    #绘制
    for j in points:
        paint_point(canvas, j.position.x + gap, j.position.y + gap)
    for j in roads:
        canvas.create_line(j.endpoint[0].position.x + gap, j.endpoint[0].position.y + gap, j.endpoint[1].position.x + gap, j.endpoint[1].position.y + gap, fill="#808080")
    for j in buildings:
        if j.direction == "v":
            canvas.create_text((j.position.x + gap, j.position.y + gap), font=(font_type, j.size), text="\n".join(j.name), fill="#000000", anchor='center')
        elif j.direction == "h":
            canvas.create_text((j.position.x + gap, j.position.y + gap), font=(font_type, j.size), text=j.name, fill="#000000", anchor='center')

    canvas.pack()

    #def location():
    #    paint_point(canvas, student.position.x + gap, student.position.y + gap, color='#FFFF00')
    #    switch = 1

    #def pause():
    #    if (switch == 0):
    #        return

    location_button = Button(map_root, text="查询所处位置", command=lambda : query.location(map_root, canvas))
    around_button = Button(map_root, text="查看周围建筑", command=lambda : query.building_around_button(map_root, canvas))
    #change_button = Button(map_root, text="更改导航策略", command=lambda : query.location(map_root, canvas))
    location_button.pack()
    around_button.pack()
    #change_button.pack()

    for j in range(len(path)-1):
        time.sleep((road[j].length//road[j].degree_of_congestion)//1.2//6)
        #student.need_time = student.need_time + ((road[j].length//road[j].degree_of_congestion)//1.2)//60
        #print((road[j].length//road[j].degree_of_congestion)*0.1)
        student.position = path[j].position
        canvas.create_line(path[j].position.x + gap, path[j].position.y + gap, path[j+1].position.x + gap, path[j+1].position.y + gap, fill="#ff0000")
        # 更新框架，强制显示改变
        map_root.update()
        #导航结束后退出（暂时）
        #pause()
        if switch == 1:
            map_root.destroy()
            return
            #break

        if j == len(path) - 2:
            map_root.destroy()
            return

    print("已经跳出")
    map_root.mainloop()
    #print("绘制结束，跳出mainloop")
    return
