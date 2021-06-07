from tkinter import *
from data import *
import initialize as init
import navigate
import query
import output


def main():
    '''数据初始化'''
    init.initialize()
  #  navigate.shortest_path_incampus_method1(student.strategy)
    '''功能选择界面'''
    navigate_button = Button(root, text="导航", command=navigate.navigate)
    query_button = Button(root, text="查询", command=query.query)
    out_button = Button(root, text="查看地图", command=output.view_campus)
    navigate_button.pack()
    query_button.pack()
    out_button.pack()
    root.mainloop()
    return


main()
