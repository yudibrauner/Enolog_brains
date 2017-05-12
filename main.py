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
options = {"no container to choose": None}
decisionMaker = None # TODO: create this class, and change this variable
there_is_no_containers = True

def addCont():
    # gets name and adds container
    name = ''
    id = ''
    rootCont = Tk()
    rootCont.wm_title("Adding container")
    contFrame = Frame(rootCont, width=300, height=500)
    contFrame.pack()
    # # Todo: print empty containers ID, print error if the user gave
    idLabel = Label(contFrame, text='container ID number in winery: ')
    idEntry = Entry(contFrame)
    idLabel.place(x=40,y=40)
    idEntry.place(x=40,y=70)

    nameLabel = Label(contFrame, text='name (wine type): ')
    nameEntry = Entry(contFrame)
    nameLabel.place(x=40,y=100)
    nameEntry.place(x=40,y=130)

    def addDetails():
        id = idEntry.get()
        name = nameEntry.get()
        container = Container(name, id)
        allContainers[id] = container
        print('-> container added')
        options[id] = name
        # TODO: to add delete "no containers..." cell if exist
        # del options["no container to choose"]
        selectedOption.set(id)  # Default
        OptionMenu(root, selectedOption, *options).place(x=110, y=20)
        rootCont.destroy()

    insertButton = Button(contFrame, text='insert details', command=addDetails)
    insertButton.place(x=40, y=200)

#GUI

root = Tk()
root.wm_title("Smart winery app")

# FRAMES:

mainFrame = Frame(root, width=1100, height=500)
mainFrame.pack()

# rightFrame = Frame(mainFrame, width=500, height=500)
# rightFrame.pack(side=RIGHT)

leftFrame = Frame(mainFrame, width=1000, height=500)
leftFrame.pack()

dataFrame = LabelFrame(leftFrame, text="data")

# IMAGES

settingsPhoto = PhotoImage(file="settings.png")
tasksPhoto = PhotoImage(file="tasks.png")
graphsPhoto = PhotoImage(file="graph.png")
addPhoto = PhotoImage(file="add.png")

#LABELS:

containerLabel = Label(leftFrame, text='Container ID:')
logLabel = Label(leftFrame, text='Log:')
temperatureLabel = Label(dataFrame, text='Temprature:')
colorLabel = Label(dataFrame, text='Color:')
densityLabel = Label(dataFrame, text='Density:')
idLabel = Label(dataFrame, text='id:')
nameLabel = Label(dataFrame, text='name:')

# BUTTONS:

addContButton = Button(leftFrame, image=addPhoto, command=addCont)
SettingsButton = Button(leftFrame, image=settingsPhoto)
tasksButton = Button(leftFrame, image=tasksPhoto)
graphsButton = Button(leftFrame, image=graphsPhoto)

# TEXTS

logText = Text (leftFrame)
temperatureText = Text (dataFrame)
colorText = Text (dataFrame)
densityText = Text (dataFrame)
idText = Text (dataFrame)
nameText = Text (dataFrame)


# DROP-DOWNS

selectedOption = StringVar()
selectedOption.set("no container to choose") # Default


# PLACES:

containerLabel.place(x=30, y=25)
OptionMenu(root, selectedOption, *options).place(x=110, y=20)
addContButton.place(x=300, y=20, height=42, width=42)

SettingsButton.place(bordermode=OUTSIDE, height=42, width=42, x=50, y=80)
tasksButton.place(bordermode=OUTSIDE, height=42, width=42, x=150, y=80)
graphsButton.place(bordermode=OUTSIDE, height=42, width=42, x=250, y=80)

logLabel.place(x=50, y=130)
logText.place(x=90, y=130, height=110, width=230)

dataFrame.place(height=150, width=270, x=50,y=240)
temperatureLabel.place(x=10, y=10)
temperatureText.place(height=25, width=70, x=90, y=10)
colorLabel.place(x=10, y=40)
colorText.place(height=25, width=70, x=90, y=40)
densityLabel.place(x=10, y=70)
densityText.place(height=25, width=70, x=90, y=70)
idLabel.place(x=190, y=0)
idText.place(height=25, width=70,x=190, y=20)
nameLabel.place(x=190, y=50)
nameText.place(height=25, width=70,x=190, y=70)

root.mainloop()
