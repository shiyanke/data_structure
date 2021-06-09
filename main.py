from tkinter import *
from data import *
import initialize as init
import navigate
import query
import output
import log


def main():
    '''数据初始化'''
    init.initialize()
    '''功能选择界面'''
    navigate_button = Button(root, text="导航", command=navigate.navigate)
    query_button = Button(root, text="查询", command=query.query)
    out_button = Button(root, text="查看地图", command=output.view_campus)
    log_button = Button(root, text="查看日志", command=log.show_log)
    navigate_button.pack()
    query_button.pack()
    out_button.pack()
    log_button.pack()
    root.mainloop()
    return


main()

