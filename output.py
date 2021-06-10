from data import *
from tkinter import *
import tkinter.messagebox
import time
import query
import log
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
    map_root = Tk()
    map_root.geometry("1000x1000")  # 设置地图窗口大小
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

    location_button = Button(map_root, text="查询所处位置", command=lambda : query.location(map_root, canvas))
    around_button = Button(map_root, text="查看周围建筑", command=lambda : query.building_around_button(map_root, canvas))
    location_button.pack()
    around_button.pack()
    query.switch = 0

    for j in range(len(path)-1):
        if query.switch == 1:
            #map_root.destroy()
            return
            #break
        if student.strategy in [1, 2, 4]:
            time.sleep((road[j].length/road[j].degree_of_congestion)/speed[0]//time_ratio_one)
        elif student.strategy == 3:
            time.sleep((road[j].length/road[j].degree_of_congestion)/speed[1]//time_ratio_one)
        canvas.create_line(path[j].position.x + gap, path[j].position.y + gap, path[j+1].position.x + gap, path[j+1].position.y + gap, fill="#ff0000")
        student.position = path[j+1].position

        log.flush_time()
        if student.which_campus == 0:
            log.save_log([str(student.time), "更新当前状态", "(" + str(student.position.x) + "," + str(student.position.y) + ")", "当前所处校区：沙河区"])
        elif student.which_campus == 1:
            log.save_log([str(student.time), "更新当前状态", "(" + str(student.position.x) + "," + str(student.position.y) + ")", "当前所处校区：海淀区"])

        # 更新框架，强制显示改变
        map_root.update()
        #导航结束后退出（暂时）

        if j == len(path) - 2:
            tkinter.messagebox.showinfo(title='提示', message='已到达，目的地在您附近')
            #map_root.destroy()
            return


    print("已经跳出")
    map_root.mainloop()
    #print("绘制结束，跳出mainloop")
    return
