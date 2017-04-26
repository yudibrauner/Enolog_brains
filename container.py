# This class represents a container of wine
import datetime


class Container:
    def __init__(self, name):
        self.name = name
        self.startDateTime = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        self.number = -1

    def setNumber(self, num):
        self.number = num

    def printContainer(self):
        print('Name: ' + str(self.name))
        print('Creation date&time: ' + str(self.startDateTime))
        print('Number: ' + str(self.number))
