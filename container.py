# This class represents a container of wine
import datetime
import random

from garbage.task import *


class Container:
    def __init__(self, _name, _id):
        self.id = _id            # number of container in winery
        # TODO: make the winery into a file and read container info from file
        # self.location = getLocation(num)  # get the location of the container by it's number from winery
        self.name = _name
        self.startDateTime = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        self.visits = list()         # a list of all the visits of the robotic arm
        self.tasks = list()          # a list of all the current armTasks for this container
        self.temperature = random.randrange(10, 50)
        self.taninns = random.randrange(10, 50)
        self.color = random.randrange(10, 50)
        self.density = random.randrange(10, 50)
        self.status = 'ready'        # statuses: ready|critical

# SETTERS:

    def setNumber(self, num):
        self.id = num

    def setName(self, _name):
        self.name = _name

# GETTERS:

    def getTemperature(self):
        return self.temperature

    def getColor(self):
        return self.color

    def getTaninns(self):
        return self.taninns

    def getDensity(self):
        return self.density

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