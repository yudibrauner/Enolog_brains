# This class represents a container of wine
import datetime
import random
from tkinter import *
from tkinter.filedialog import *
# from new_main_II import *
import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use("TKAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation


NO_DETAILS = "N/A"
EMPTY_IMAGE = "images/container.png"
FULL_IMAGE = "images/containerAct.png"


class Container:
    def __init__(self, _id, _place, root):
        self.id = _id            # number of container in winery
        self.frame = root
        self.startDateTime = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        self.tasks = list()
        self.temperature = StringVar()
        self.tannins = StringVar()
        self.color = StringVar()
        self.density = StringVar()
        self.name = StringVar()
        self.densityLabel = None
        self.buttonFunction = self.addCont
        self.isFull = False
        self.place = _place
        self.image = None
        self.photo = None
        self.idLabel = None
        self.densityValLabel = None
        self.tanninsValLabel = None
        self.colorValLabel = None
        self.temperatureValLabel = None
        self.nameLabel = None
        self.initParams()
        self.frame.grid(row=0, column=0, columnspan=2)
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)

    def setImage(self):
        self.photo = PhotoImage(file=self.image)
        contButton = Button(self.frame, height=44, width=52, image=self.photo, relief=FLAT, background='#810d2b', command=self.buttonFunction)
        contButton.place(x=self.place[0], y=self.place[1])

    def initLabels(self):
        self.idLabel = Label(self.frame, text=str(self.id) + ': ', background='#810d2b')
        self.idLabel.place(x=self.place[0] + 10, y=self.place[1] - 30)

        self.nameLabel = Label(self.frame, text='Name: ', background='#810d2b')
        self.nameLabel.place(x=self.place[0] + 5, y=self.place[1] + 70)
        self.nameLabel = Label(self.frame, textvariable=str(self.name), background='#810d2b')
        self.nameLabel.place(x=self.place[0] + 25, y=self.place[1] - 30)

        self.densityLabel = Label(self.frame, text='Dns: ', background='#810d2b')
        self.densityLabel.place(x=self.place[0] + 5, y=self.place[1] + 70)
        self.densityValLabel = Label(self.frame, textvariable=str(self.density), background='#810d2b')
        self.densityValLabel.place(x=self.place[0] + 35, y=self.place[1] + 70)

        self.tanninsValLabel = Label(self.frame, text='Tnn: ', background='#810d2b')
        self.tanninsValLabel.place(x=self.place[0] + 5, y=self.place[1] + 90)
        self.tanninsValLabel = Label(self.frame, textvariable=str(self.tannins), background='#810d2b')
        self.tanninsValLabel.place(x=self.place[0] + 35, y=self.place[1] + 90)

        self.colorValLabel = Label(self.frame, text='Clr: ', background='#810d2b')
        self.colorValLabel.place(x=self.place[0] + 5, y=self.place[1] + 110)
        self.colorValLabel = Label(self.frame, textvariable=str(self.color), background='#810d2b')
        self.colorValLabel.place(x=self.place[0] + 35, y=self.place[1] + 110)

        self.temperatureValLabel = Label(self.frame, text='Tmp: ', background='#810d2b')
        self.temperatureValLabel.place(x=self.place[0] + 5, y=self.place[1] + 130)
        self.temperatureValLabel = Label(self.frame, textvariable=str(self.temperature), background='#810d2b')
        self.temperatureValLabel.place(x=self.place[0] + 35, y=self.place[1] + 130)

    def initParams(self):
        self.temperature.set(NO_DETAILS)
        self.tannins.set(NO_DETAILS)
        self.color.set(NO_DETAILS)
        self.density.set(NO_DETAILS)
        self.name.set(NO_DETAILS)
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
        self.tannins.set(random.randrange(10, 50))
        self.color.set(random.randrange(10, 50))
        self.density.set(random.randrange(10, 50))

    def addDetails(self, rootCont, nameEntry):
        name = nameEntry.get()
        if name:
            self.name.set(name)
            self.fillContainer()
            self.buttonFunction = self.showDetails
            print('-> container added')
            rootCont.destroy()

    def addCont(self):
        rootCont = Tk()
        rootCont.wm_title("Adding container " + str(self.id))
        contFrame = Frame(rootCont, width=300, height=500)
        contFrame.pack()
        nameLabel = Label(contFrame, text='name (wine type): ')
        nameEntry = Entry(contFrame)
        nameLabel.place(x=40, y=100)
        nameEntry.place(x=40, y=130)

        insertButton = Button(contFrame, text='insert details', command=lambda: self.addDetails(rootCont, nameEntry))
        insertButton.place(x=40, y=200)

    def clearAllVariables(self, rootCont):
        Container(self.id, self.place, self.frame)
        self.id = NO_DETAILS
        self.temperature.set(None)
        self.tannins.set(None)
        self.color.set(None)
        self.density.set(None)
        self.name.set(None)
        self.idLabel.place_forget()
        self.nameLabel.place_forget()
        self.temperatureValLabel.place_forget()
        self.tanninsValLabel.place_forget()
        self.colorValLabel.place_forget()
        self.densityValLabel.place_forget()
        rootCont.destroy()

    def endProcess(self, rootCont):
        msgBox = messagebox.askyesno('End Process ' + str(self.id) + ': ' + str(self.name.get()), 'Are you sure you want to end this process?', master=rootCont)
        if msgBox:
            self.clearAllVariables(rootCont)
            print('-> process ended')

    def showDetails(self):
        rootCont = Tk()
        rootCont.attributes("-topmost", 1)
        rootCont.wm_title("Container " + str(self.id) + ': ' + str(self.name.get()))
        contFrame = Frame(rootCont, width=1000, height=500)
        contFrame.pack()

        canvas = FigureCanvasTkAgg(self.f, contFrame)
        #canvas.show()
        canvas.get_tk_widget().pack(side=tk.RIGHT, expand=True)
        ani = animation.FuncAnimation(self.f, self.animate, interval=500)
        endProcessButton = Button(contFrame, text='End Process', command=lambda: self.endProcess(rootCont))
        endProcessButton.place(x=40, y=20)
        rootCont.mainloop()

    def animate(self, i):
        pullData = open('data.txt', 'r').read()
        dataList = pullData.split('\n')
        xList = []
        yList = []
        for eachLine in dataList:
            if len(eachLine) > 1:
                x, y = eachLine.split(',')
                xList.append(int(x))
                yList.append(int(y))
        self.a.clear()
        self.a.plot(xList, yList)


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
        print('Name: ' + str(self.name.get()))
        print('Winery Container Number: ' + str(self.id))
        print('Creation date&time: ' + str(self.startDateTime))
        print('Tasks: ' + self.tasksToString())
        print('Temperature: ' + str(self.temperature.get()) + '°C')
