from tkinter import *
from data import *
import initialize as init
import navigate
import query


def main():
    '''数据初始化'''
    init.initialize()
    '''功能选择界面'''
    navigate_button = Button(root, text="导航", command=navigate.navigate)
    query_button = Button(root, text="查询", command=query.query)
    navigate_button.pack()
    query_button.pack()
    root.mainloop()
    return


main()
