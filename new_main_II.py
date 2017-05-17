from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time

from container import *
from taskPlan import *
from emptyContainer import *

# INIT TASKS :TODO: move it to another class, for there won't be mess

#short:
short = {}
short['color'] = [1,2,2.5,2.8,3,3,4,4,3.7,3.7,3.5,3.5]
short['taninns'] = [5,8,10,12,16,20,24,28,32,38,44,50]
short['temperature'] = [1,2,4,6,8,9,7,6,5,4,2,1]
short['density'] = [1110,1105,1095,1080,1065,1045,1030,
                    1020,1010,1005,1000,995]

#middle
normal = {}
normal['color'] = [1,1.2,1.6,2,2.4,3,3.4,3.8,3.8,3.6,3.6,3.4,3.4,3.2,
                   3.2,3.2,3.2,3.1,3.1,3]
normal['taninns'] = [5,5,7,10,12,15,17,20,22,25,28,31,35,39,43,47,52,57,62,67]
normal['temperature'] = [0.5,1,2,4,5,6,7,7,6,5,4,3,3,2,2,1,1,1,0.5,0.5]
normal['density'] = [1110,1105,1100,1095,1090,1080,1070,1055,1030,
                     1020,1015,1010,1005,1002,1000,998,996,996,994,994]

long = {}
long['color'] = [1,1.2,1.4,1.6,1.8,2,2.3,2.5,2.8,3.1,3.4,3.4,3.4,3.3,
                 3.3,3.3,3.3,3.2,3.2,3.2,3.1,3.1,3.1,3,3,2.9,2.9,2.8]
long['taninns'] = [5,5,5,7,8,10,12,14,16,18,20,22,24,26,28,30,33,36,39,43,47,52,57,62,67,72,77,82]
long['temperature'] = [0.5,0.5,1,1,2,2,3,3,4,4,5,5,5,4,3,3,2,2,2,1,1,1,1,1,0.5,0.5,0.5,0.5]
long['density'] = [1110,1110,1108,1105,1102,1098,1092,1087,1075,1060,1045,1035,1028,
                   1022,1018,1015,1012,1010,1008,1006,1004,1002,1000,999,998,997,996,995]


#INIT:

tasks = {}
allContainers = []
labelsContainers = {}

tasks['long'] = TaskPlan("long", long, 14)
tasks['normal'] = TaskPlan("normal", normal, 10)
tasks['short'] = TaskPlan("short", short, 7)

#GUI

root = Tk()
root.wm_title("Smart winery app")

emptyImage = PhotoImage(file="container.png")
fullImage = PhotoImage(file="containerAct.png")


# FRAMES:

mainFrame = Frame(root, width=1000, height=600, bg='#810d2b')
mainFrame.pack()

# creating all the containers
curID = 0
for i in range(0,10):
    for j in range(0,2):
        id = curID
        place = (85 * i + 70, 220*j + 50)
        allContainers.append(EmptyContainer(id, place, emptyImage, fullImage))
        curID += 1

# it's refreshing the screen TODO: how should we do that automatically, without a button?
def refreshScreen():
    for i in range (0, len(allContainers)):
        cont = allContainers[i]
        labelsContainers[i] = {}
        contButton = Button(mainFrame, image=cont.getImage(), relief=FLAT, background='#810d2b',
                            command=cont.buttonFunction)
        contButton.place(x=cont.getPlace()[0], y=cont.getPlace()[1])
        labelsContainers[i]['id'] = Label(mainFrame, text="id: " + str(cont.getId()))
        labelsContainers[i]['density'] = Label(mainFrame, text="de: " + str(cont.getDensity()),
                                                   background='#810d2b')
        labelsContainers[i]['taninns'] = Label(mainFrame, text="ta: " + str(cont.getTaninns()),
                                                   background='#810d2b')
        labelsContainers[i]['color'] = Label(mainFrame, text="co: " + str(cont.getColor()),
                                                 background='#810d2b')
        labelsContainers[i]['temperature'] = Label(mainFrame, text="te: " + str(cont.getTemperature()),
                                                       background='#810d2b')
        labelsContainers[i]['id'].place(x=cont.getPlace()[0] + 10, y=cont.getPlace()[1] - 30)
        labelsContainers[i]['density'].place(x=cont.getPlace()[0] + 10, y=cont.getPlace()[1] + 70)
        labelsContainers[i]['taninns'].place(x=cont.getPlace()[0] + 10, y=cont.getPlace()[1] + 90)
        labelsContainers[i]['color'].place(x=cont.getPlace()[0] + 10, y=cont.getPlace()[1] + 110)
        labelsContainers[i]['temperature'].place(x=cont.getPlace()[0] + 10, y=cont.getPlace()[1] + 130)


refreshButton = Button(mainFrame, text="refresh", relief=FLAT, command=refreshScreen)
refreshButton.place(x=400, y=500)
refreshScreen()

root.mainloop()
