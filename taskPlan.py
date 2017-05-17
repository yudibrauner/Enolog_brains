# This class is a task for the robotic arm or the container
from container import *

from garbage.roboticArm import *

class TaskPlan:
    def __init__(self, taskName, listsOfParams, length):
        self.task = taskName
        self.list = listsOfParams
        self.length = length

    def toString(self):
        print(self.task + " => " + str(self.list) + " <= " + str(self.length))

    def printStatistic(self):
        print("TODO")

# GETTERS

    def getColor(self):
        return self.list['color']

    def getDensity(self):
        return self.list['density']

    def getTaninns(self):
        return self.list['taninns']

    def getTemperature(self):
        return self.list['temperature']