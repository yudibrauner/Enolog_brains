from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time

from container import *

#INIT:
allContainers = {}
decisionMaker = None # TODO: create this class, and change this variable



def nothing(): #TODO: delete this in the end
    x = 3

def addCont():
    # gets name and adds container
    id = input('container ID number in winery: ')
    # Todo: print empty containers ID, print error if the user gave
    name = input('name (wine type): ')
    init_priority = input('initial priority: ')
    container = Container(name, id)
    allContainers[id] = container
    print('-> container added')





#GUI

root = Tk()
root.wm_title("smart winery app")

# FRAMES:

mainFrame = Frame(root, width=1100, height=500)
mainFrame.pack()

rightFrame = Frame(mainFrame, width=500, height=500)
rightFrame.pack(side=RIGHT)

leftFrame = Frame(mainFrame, width=500, height=500)
leftFrame.pack(side=LEFT)


#LABELS:

global containerLabel
containerLabel=Label(leftFrame, text='Container')


# BUTTONS:

addContButton = Button(leftFrame, text="Initialize wine", command=addCont)
SettingsButton = Button(leftFrame, text='Settings')
tasksButton = Button(leftFrame, text='Tasks edit')
graphsButton = Button(leftFrame, text='Graphs')





# PACKS:

addContButton.pack(side=LEFT)
containerLabel.pack(side=TOP)
SettingsButton.pack(side=TOP)
tasksButton.pack(side=TOP)
graphsButton.pack(side=TOP)





# menu=Menu(root)
# root.config(menu=menu)
# subMenu1 = Menu(menu)
# menu.add_cascade(label="file", menu=subMenu1)
# subMenu1.add_command(label="Open text", command=nothing)
# subMenu1.add_command(label="Save as", command=nothing)
# subMenu1.add_separator()
# subMenu1.add_command(label="open simulator", command=nothing)
# subMenu1.add_command(label="exit", command=exit)
# subMenu2 = Menu(menu)
# menu.add_cascade(label="actions", menu=subMenu2)
# subMenu2.add_command(label="print containers", command=nothing)
# subMenu2.add_command(label="add container", command=nothing)
# subMenu2.add_command(label="add task", command=nothing)
# subMenu2.add_command(label="remove container", command=nothing)
# subMenu2.add_command(label="move robotic hand", command=nothing)
# subMenu2.add_command(label="set home position", command=nothing)
# subMenu2.add_command(label="start winery", command=nothing)
# subMenu3=Menu(menu)
# menu.add_cascade(label="containers", menu=subMenu3)
# subMenu4=Menu(menu)
# menu.add_cascade(label="help", menu=subMenu4)
# subMenu4.add_command(label="About", command=nothing)


root.mainloop()
