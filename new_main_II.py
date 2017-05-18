from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time
from taskPlan import *
from container import *
from exampleTasks import *

#INIT:

tasks = {}
allContainers = []
labelsContainers = {}

# tasks['long'] = TaskPlan("long", exampleTasks.getLong(), 14)
# tasks['normal'] = TaskPlan("normal", exampleTasks.getNormal(), 10)
# tasks['short'] = TaskPlan("short", exampleTasks.getShort(), 7)

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
        allContainers.append(Container(id, place, mainFrame))
        curID += 1


root.mainloop()
