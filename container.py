# This class represents a container of wine
import datetime
import random
from tkinter import *
from tkinter.filedialog import *
# from new_main_II import *
import tkinter as tk

NO_DETAILS = "N/A"
EMPTY_IMAGE = "images/container.png"
FULL_IMAGE = "images/containerAct.png"


class Container:
    def __init__(self, _id, _place, root):
        self.id = _id            # number of container in winery
        # TODO: make the winery into a file and read container info from file
        self.frame = root
        self.startDateTime = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        self.tasks = list()
        self.temperature = StringVar()
        self.taninns = StringVar()
        self.color = StringVar()
        self.density = StringVar()
        self.buttonFunction = self.addCont
        self.isFull = False
        self.place = _place
        self.image = None
        self.photo = None
        self.idLabel = None
        self.densityLabel = None
        self.tanninsLabel = None
        self.colorLabel = None
        self.temperatureLabel = None
        self.initParams()
        self.frame.grid(row=0,column=0,columnspan=2)

    def setImage(self):
        self.photo = PhotoImage(file=self.image)
        contButton = Button(self.frame, height=44, width=52, image=self.photo, relief=FLAT, background='#810d2b', command=self.buttonFunction)
        contButton.place(x=self.place[0], y=self.place[1])

    def initLabels(self):
        self.idLabel = Label(self.frame, text="id: " + str(self.id), background='#810d2b')
        self.idLabel.place(x=self.place[0] + 10, y=self.place[1] - 30)

        self.densityLabel = Label(self.frame, textvariable=str(self.density), background='#810d2b')
        self.densityLabel.place(x=self.place[0] + 10, y=self.place[1] + 70)

        self.tanninsLabel = Label(self.frame, textvariable="ta: " + str(self.taninns), background='#810d2b')
        self.tanninsLabel.place(x=self.place[0] + 10, y=self.place[1] + 90)

        self.colorLabel = Label(self.frame, textvariable="co: " + str(self.color), background='#810d2b')
        self.colorLabel.place(x=self.place[0] + 10, y=self.place[1] + 110)

        self.temperatureLabel = Label(self.frame, textvariable="te: " + str(self.temperature), background='#810d2b')
        self.temperatureLabel.place(x=self.place[0] + 10, y=self.place[1] + 130)

    def initParams(self):
        self.temperature.set(NO_DETAILS)
        self.taninns.set(NO_DETAILS)
        self.color.set(NO_DETAILS)
        self.density.set(NO_DETAILS)
        self.image = EMPTY_IMAGE
        self.setImage()
        self.initLabels()

    def fillContainer(self):
        self.updateParams()
        self.isFull = True
        self.image = FULL_IMAGE
        self.buttonFunction = self.showDetails
        self.setImage()

    def updateParams(self):
        self.temperature.set(random.randrange(10, 50))
        self.taninns.set(random.randrange(10, 50))
        self.color.set(random.randrange(10, 50))
        self.density.set(random.randrange(10, 50))

    def addCont(self):
        rootCont = Tk()
        rootCont.wm_title("Adding container " + str(self.id))
        contFrame = Frame(rootCont, width=300, height=500)
        contFrame.pack()
        nameLabel = Label(contFrame, text='name (wine type): ')
        nameEntry = Entry(contFrame)
        nameLabel.place(x=40, y=100)
        nameEntry.place(x=40, y=130)

        def addDetails():
            name = nameEntry.get()
            if name:
                self.name = name
                self.fillContainer()
                self.buttonFunction = self.showDetails
                print('-> container added')
                rootCont.destroy()
        insertButton = Button(contFrame, text='insert details', command=addDetails)
        insertButton.place(x=40, y=200)

    def showDetails(self):
        rootCont = Tk()
        rootCont.wm_title("details of container " + str(self.id))
        contFrame = Frame(rootCont, width=300, height=500)
        contFrame.pack()

    # SETTERS:

    def setNumber(self, num):
        self.id = num

    def setName(self, _name):
        self.name = _name


# OTHER FUNCTIONS:

    def cool(self):
        self.temperature -= 5

    def regulate(self): #TODO : ask Shivi how the regulator affects the color, density...
        print("there's nothing yet")

    def addTask(self, taskName):
        if taskName in TASK_NAMES:
            task = Task(taskName)
            self.tasks.append(task)
        else:
            print('-> ERROR: not a task')

    def tasksToString(self):
        lst = ''
        for t in self.tasks:
            lst += str(t.task) + ','
        return lst

    def printContainer(self):
        print('Name: ' + str(self.name))
        print('Winery Container Number: ' + str(self.id))
        print('Creation date&time: ' + str(self.startDateTime))
        print('Tasks: ' + self.tasksToString())
        print('Temperature: ' + str(self.temperature) + '°C')
        print('Status: ' + str(self.status))