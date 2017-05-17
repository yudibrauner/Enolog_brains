# This class represents a container of wine
import datetime
import random
from tkinter import *
from tkinter.filedialog import *
# from new_main_II import *
from garbage.taskGarbage import *


class EmptyContainer:
    def __init__(self, _id, _place, empty_image, full_image):
        self.id = _id            # number of container in winery
        # TODO: make the winery into a file and read container info from file
        self.startDateTime = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        self.visits = list()         # a list of all the visits of the robotic arm
        self.tasks = list()          # a list of all the current armTasks for this container
        self.NO_DETAIL = "N/A"
        self.temperature = self.NO_DETAIL
        self.taninns = self.NO_DETAIL
        self.color = self.NO_DETAIL
        self.density = self.NO_DETAIL
        self.status = 'empty'        # statuses: ready|critical
        self.place = _place
        self.emptyImage = empty_image
        self.fullImage = full_image
        self.image = self.emptyImage
        self.buttonFunction = self.addCont


    def addCont(self):
        rootCont = Tk()
        rootCont.wm_title("Adding container " + str(self.id))
        contFrame = Frame(rootCont, width=300, height=500)
        contFrame.pack()
        # # Todo: print empty containers ID, print error if the user gave an ID tha does not exist
        nameLabel = Label(contFrame, text='name (wine type): ')
        nameEntry = Entry(contFrame)
        nameLabel.place(x=40, y=100)
        nameEntry.place(x=40, y=130)
        def addDetails():
            name = nameEntry.get()
            if name:
                self.name = name
                self.image = self.fullImage
                self.temperature = random.randrange(10, 50)
                self.taninns = random.randrange(10, 50)
                self.color = random.randrange(10, 50)
                self.density = random.randrange(10, 50)
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

# GETTERS:

    def getImage(self):
        return self.image

    def getPlace(self):
        return self.place

    def getTemperature(self):
        return self.temperature

    def getColor(self):
        return self.color

    def getTaninns(self):
        return self.taninns

    def getDensity(self):
        return self.density

    def getId(self):
        return self.id

    def getName(self):
        return self.name

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