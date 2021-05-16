from data import *
from tkinter import *


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


def imaging(one_campus):  #校区临时绘图
    map_root = Tk()
    map_root.geometry("1000x600")  # 设置地图窗口大小
    canvas = Canvas(map_root, bg='white')
    canvas.config(width=400 + 2 * gap, height=575 + 2 * gap)  # 画布大小
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
