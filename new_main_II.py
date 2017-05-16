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
