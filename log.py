from tkinter import *
from data import *
import datetime


def save_log(list_item):
    string = ""
    i = 1
    for item in list_item:
        string += str(item)
        if i != len(list_item):
            string += " "
        else:
            string += "\n"
        i += 1
    log_file = open("log.txt", 'a')
    log_file.write(string)
    return True


def show_log():
    log_file = open("log.txt", 'r')
    root = Tk()
    sb = Scrollbar(root)
    sb.pack(side=RIGHT, fill=Y)
    lb = Listbox(root, width=100, height=20, yscrollcommand=sb.set)
    for line in log_file.readlines():
        lb.insert(END, line)
    lb.pack(side=LEFT, fill=BOTH)
    sb.config(command=lb.yview)
    root.mainloop()
    log_file.close()
    return


def flush_time():
    now = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    delta_time = now - student.star_time
    secs = to_s(str(delta_time)) * time_ratio_one + to_s(str(student.star_time.hour)+":"+str(student.star_time.minute)+":"+str(student.star_time.second))
    minute, second = (secs // 60, secs % 60)
    hour = 0
    if minute > 60:
        hour, minute = (minute // 60, minute % 60)
    student.time = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, hour, minute, second)
    return


def to_s(t):
    h, m, s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)
