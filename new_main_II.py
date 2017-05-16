from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time

from container import *
from emptyContainer import *

#INIT:

allContainers = []
labelsContainers = {}


# creating all the containers
curID = 0
for i in range(0,10):
    for j in range(0,2):
        id = curID
        place = (60 * i + 70, 220*j + 50)
        # allContainers[id] = EmptyContainer(id, place, mainFrame)
        # allContainers[id] = EmptyContainer(id, place, emptyImage)
        allContainers.append(EmptyContainer(id, place))
        curID += 1



#GUI

root = Tk()
root.wm_title("Smart winery app")

emptyImage = PhotoImage(file="container.png")
fullImage = PhotoImage(file="containerAct.png")


# FRAMES:

mainFrame = Frame(root, width=1000, height=600, bg='#810d2b')
mainFrame.pack()


def refreshScreen():
    print(allContainers)
    for i in range (0, len(allContainers)):
        cont = allContainers[i]
        contButton = Button(mainFrame, image=emptyImage, relief=FLAT, background='#810d2b',
                            command=cont.addCont)
        labelsContainers[curID]['id'] = Label(mainFrame, text="id: " + str(cont.getId()))
        labelsContainers[curID]['density'] = Label(mainFrame, text="de: " + str(cont.getDensity()),
                                                   background='#810d2b')
        labelsContainers[curID]['taninns'] = Label(mainFrame, text="ta: " + str(cont.getTaninns()),
                                                   background='#810d2b')
        labelsContainers[curID]['color'] = Label(mainFrame, text="co: " + str(cont.getColor()),
                                                 background='#810d2b')
        labelsContainers[curID]['temperature'] = Label(mainFrame, text="te: " + str(cont.getTemperature()),
                                                       background='#810d2b')
        labelsContainers[curID]['id'].place(x=place[0] + 10, y=place[1] - 30)
        labelsContainers[curID]['density'].place(x=place[0] + 10, y=place[1] + 70)
        labelsContainers[curID]['taninns'].place(x=place[0] + 10, y=place[1] + 90)
        labelsContainers[curID]['color'].place(x=place[0] + 10, y=place[1] + 110)
        labelsContainers[curID]['temperature'].place(x=place[0] + 10, y=place[1] + 130)

refreshScreen()

root.mainloop()
