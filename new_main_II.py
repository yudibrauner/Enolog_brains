from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time
from taskPlan import *
from emptyContainer import *

# INIT TASKS :

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

# GUI

root = Tk()
root.wm_title("Smart winery app")

# FRAMES:

mainFrame = Frame(root, width=1000, height=600, bg='#810d2b')
mainFrame.pack()

def settings(self):
    rootCont = Tk()
    rootCont.wm_title("Settings")
    contFrame = Frame(rootCont, width=300, height=500)
    contFrame.pack()
    nameLabel = Label(contFrame, text='Set number of containers: ')
    nameEntry = Entry(contFrame, text=str(len(allContainers)))
    nameLabel.place(x=40, y=100)
    nameEntry.place(x=40, y=130)

    def addDetails():
        name = nameEntry.get()
        if name:
            self.name = name
            self.buttonFunction = self.showDetails
            self.fillContainer()
            print('-> container added')
            rootCont.destroy()

    insertButton = Button(contFrame, text='insert details', command=addDetails)
    insertButton.place(x=40, y=200)

settingsButton = Button(mainFrame, text='settings', command=settings)
settingsButton.place(x=40, y=200)
# creating all the containers
curID = 0
for i in range(0, 5):
    for j in range(0, 2):
        id = curID
        place = (170 * i + 150, 250*j + 100)
        allContainers.append(EmptyContainer(id, place, mainFrame))
        curID += 1


root.mainloop()
