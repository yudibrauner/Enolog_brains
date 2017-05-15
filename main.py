from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time

from container import *

#INIT:
NO_CONTAINERS = "No Containers"
allContainers = {}
options = {NO_CONTAINERS: None}
CURRENT_CONTAINER = NO_CONTAINERS              # this variable contains the current container showed in frame
decisionMaker = None                                   # TODO: create this class, and change this variable
there_is_no_containers = True


def addCont():
    name = ''
    id = ''
    rootCont = Tk()
    rootCont.wm_title("Adding container")
    contFrame = Frame(rootCont, width=300, height=500)
    contFrame.pack()
    # # Todo: print empty containers ID, print error if the user gave an ID tha does not exist
    idLabel = Label(contFrame, text='container ID number in winery: ')
    idEntry = Entry(contFrame)
    idLabel.place(x=40, y=40)
    idEntry.place(x=40, y=70)

    nameLabel = Label(contFrame, text='name (wine type): ')
    nameEntry = Entry(contFrame)
    nameLabel.place(x=40, y=100)
    nameEntry.place(x=40, y=130)

    def addDetails():
        if NO_CONTAINERS in options:
            del options[NO_CONTAINERS]
        id = idEntry.get()
        name = nameEntry.get()
        if id and name:
            container = Container(name, id)
            allContainers[id] = container
            print('-> container added')
            options[id] = name
            selectedOption.set(id)  # Default
            OptionMenu(root, selectedOption, *options).place(x=110, y=20)
            rootCont.destroy()

    insertButton = Button(contFrame, text='insert details', command=addDetails)
    insertButton.place(x=40, y=200)


def removeCont():
    global CURRENT_CONTAINER
    del options[CURRENT_CONTAINER]
    if not options.items():
        options[NO_CONTAINERS] = None
    CURRENT_CONTAINER = list(options.keys())[0]
    selectedOption.set(CURRENT_CONTAINER)
    OptionMenu(root, selectedOption, *options).place(x=110, y=20)

    print('-> container has been removed')


def selectContainerEvent(*args):
    global CURRENT_CONTAINER
    CURRENT_CONTAINER = selectedOption.get()
    print(str(CURRENT_CONTAINER))


#GUI

root = Tk()
root.wm_title("Smart winery app")

# FRAMES:

mainFrame = Frame(root, width=370, height=450, bg='#810d2b')
mainFrame.pack()

# rightFrame = Frame(mainFrame, width=500, height=500)
# rightFrame.pack(side=RIGHT)

#leftFrame = Frame(mainFrame, width=350, height=420, bg='#810d2b')
#leftFrame.pack()

dataFrame = LabelFrame(mainFrame, text="data")

# IMAGES

settingsPhoto = PhotoImage(file="settings.png")
tasksPhoto = PhotoImage(file="tasks.png")
graphsPhoto = PhotoImage(file="graph.png")
addPhoto = PhotoImage(file="add.png")

# LABELS:

containerLabel = Label(mainFrame, text='Container ID:', background='#810d2b')
logLabel = Label(mainFrame, text='Log:', background='#810d2b')
temperatureLabel = Label(dataFrame, text='Temperature:', background='#810d2b')
colorLabel = Label(dataFrame, text='Color:', background='#810d2b')
densityLabel = Label(dataFrame, text='Density:', background='#810d2b')
idLabel = Label(dataFrame, text='id:', background='#810d2b')
nameLabel = Label(dataFrame, text='name:', background='#810d2b')

# BUTTONS:

addContButton = Button(mainFrame, image=addPhoto, relief=FLAT, background='#810d2b', command=addCont)
SettingsButton = Button(mainFrame, image=settingsPhoto, relief=FLAT, background='#810d2b')  # , highlightbackground='#f3f3f3'
tasksButton = Button(mainFrame, image=tasksPhoto, relief=FLAT, background='#810d2b')
graphsButton = Button(mainFrame, image=graphsPhoto, relief=FLAT, background='#810d2b')
removeButton = Button(mainFrame, text='Remove This Container', command=removeCont, relief=FLAT, background='#810d2b')

# TEXTS

logText = Text(mainFrame)
temperatureText = Text(dataFrame)
colorText = Text(dataFrame)
densityText = Text(dataFrame)
idText = Text(dataFrame)
nameText = Text(dataFrame)


# DROP-DOWNS

selectedOption = StringVar()
selectedOption.trace('w', selectContainerEvent)
selectedOption.set(NO_CONTAINERS)  # Default


# PLACING:

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
idText.place(height=25, width=70, x=190, y=20)
nameLabel.place(x=190, y=50)
nameText.place(height=25, width=70, x=190, y=70)

removeButton.place(bordermode=OUTSIDE, x=110, y=400)

root.mainloop()
