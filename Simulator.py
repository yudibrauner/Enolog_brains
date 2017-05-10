from container import *
from allContainers import *
from task import *
from winery import *

from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time


class Simulator:
    def __init__(self, _robArm, _containers, _winery):
        robArm = _robArm
        containers = _containers
        winery = _winery


        root = Tk()
        topFrame = Frame(root, width=1300, height=550)
        # bottomFrame = Frame()
        topFrame.pack()
        # bottomFrame.pack(side=BOTTOM)
        global l1
        l1=Label(root, text='simulator')
        l1.pack()

        menu=Menu(root)
        root.config(menu=menu)

        subMenu1 = Menu(menu)
        menu.add_cascade(label="file", menu=subMenu1)

        subMenu2 = Menu(menu)
        menu.add_cascade(label="actions", menu=subMenu2)

        subMenu3=Menu(menu)
        menu.add_cascade(label="containers", menu=subMenu3)


        subMenu4=Menu(menu)
        menu.add_cascade(label="help", menu=subMenu4)


        e1 = Entry(root)

        root.mainloop()
