# This class is a task for the robotic arm or the container
from roboticArm import *
from container import *


TASK_NAMES = ('stir', 'color', 'temperature')


class Task:
    def __init__(self, taskName):
        self.task = taskName

    def startTask(self):
        if self.task == 'stir':
            RoboticArm.stir()
        elif self.task == 'color':
            RoboticArm.getColor()
        elif self.task == 'temperature':
            Container.getTemperature()

    @staticmethod
    def printAllTasks():
        print('Task list: ' + str(TASK_NAMES))
