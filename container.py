# This class represents a container of wine
import datetime


class Container:
    def __init__(self, name, num, priority=100):
        self.number = num            # number of container in winery
        # TODO: make the winery into a file and read container info from file
        # self.location = getLocation(num)  # get the location of the container by it's number from winery
        self.name = name
        self.priority = priority
        self.startDateTime = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        self.visits = list()         # a list of all the visits of the robotic arm
        self.tasks = list()          # a list of all the current armTasks for this container

    def setNumber(self, num):
        self.number = num

    def addTask(self, task):
        self.tasks.append(task)

    def printContainer(self):
        print('Name: ' + str(self.name))
        print('Winery Container Number: ' + str(self.number))
        print('Creation date&time: ' + str(self.startDateTime))
        print('Priority: ' + str(self.priority))
        print('Tasks: ' + str(self.tasks))
