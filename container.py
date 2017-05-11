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
        self.temperature = self.getTemperature()
        self.color = self.getColor()
        self.density = self.getDensity()
        self.status = 'ready'        # statuses: ready|critical

    def setNumber(self, num):
        self.id = num

    def addTask(self, taskName):
        if taskName in TASK_NAMES:
            task = Task(taskName)
            self.tasks.append(task)
        else:
            print('-> ERROR: not a task')

    def getTemperature(self):
        return random.randrange(10, 50)

    def getColor(self):
        return random.randrange(10, 50)

    def getDensity(self):
        return random.randrange(10, 50)

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
