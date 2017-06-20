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
num_of_containers = 10

ANIMATION_INTERVAL = 0.5
# tasks['long'] = TaskPlan("long", exampleTasks.getLong(), 14)
# tasks['normal'] = TaskPlan("normal", exampleTasks.getNormal(), 10)
# tasks['short'] = TaskPlan("short", exampleTasks.getShort(), 7)

# GUI

root = Tk()
root.wm_title("Smart winery app")

# FRAMES:

mainFrame = Frame(root, width=1000, height=600, bg='#810d2b')
mainFrame.pack()


def settings():
    #  TODO: fix up this popup
    rootCont = Tk()
    rootCont.wm_title("Settings")
    contFrame = Frame(rootCont, width=300, height=500)
    contFrame.pack()
    numOfContainersLabel = Label(contFrame, text='Set number of containers: ')
    numOfContainersEntry = Entry(contFrame, text=str(num_of_containers))
    sensorsIntervalLabel = Label(contFrame, text='Set Sensors Interval (sec): ')
    sensorsIntervalEntry = Entry(contFrame, text=str(ANIMATION_INTERVAL))
    numOfContainersLabel.place(x=40, y=100)
    numOfContainersEntry.place(x=40, y=130)
    sensorsIntervalLabel.place(x=40, y=160)
    sensorsIntervalEntry.place(x=40, y=190)

    def addDetails():
        numOfContainers = numOfContainersEntry.get()
        ANIMATION_INTERVAL = sensorsIntervalEntry.get()
        for container in allContainers:
            container.setInterval(ANIMATION_INTERVAL)
            if container.isFull:
                container.generator.setInterval(ANIMATION_INTERVAL)
        print('->  Number of containers set to: ' + numOfContainers)
        print('->  Sensors Interval set to: ' + ANIMATION_INTERVAL)
        rootCont.destroy()

    cancelButton = Button(contFrame, text='Cancel', command=rootCont.destroy)
    cancelButton.place(x=40, y=300)
    insertButton = Button(contFrame, text='OK', command=addDetails)
    insertButton.place(x=150, y=300)


def swapNewForOldContainer(old_id, new_container):
    for container in allContainers:
        if container.id == old_id:
            allContainers.remove(container)
    allContainers.append(new_container)


settingsButton = Button(mainFrame, text='settings', command=settings)
settingsButton.place(x=10, y=10)
# creating all the containers
for i in range(0, 5):
    for j in range(0, 2):
        id = (i+1)*(j+1)
        place = (170 * i + 150, 250*j + 100)
        allContainers.append(Container(id, place, mainFrame, ANIMATION_INTERVAL))


root.mainloop()
