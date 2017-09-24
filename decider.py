from container import *
from data_generator import  *


class Decider:

    # def __init__(self, container, fermentation, fermentation_file):
    #     self.fermentation_program = fermentation
    #     self.fermentation_file = fermentation_file
    #     self.times = list()
    #     self.tannins = list()
    #     self.color = list()
    #     self.density = list()
    #     self.cool = list()

    def __init__(self, container):
        self.container = container
        self.countProblems = 0
        # self.times = list()
        # self.tannins = list()
        # self.color = list()
        # self.density = list()
        # self.cool = list()

    def setNewData(self, new_time, tannins, color, density, cool):
        self.times.append(new_time)
        self.tannins.append(tannins)
        self.color.append(color)
        self.density.append(density)
        self.cool.append(cool)
        self.calculateTrend()

    def calculateTrend(self):
        # TODO: calculate trend from new data and from expected data and compare
        # https://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
        # https://www.mathworks.com/help/matlab/ref/polyfit.html
        print('does nothing at the moment')

    def decide(self):
        self.currentValues = {"density": self.container.attr("density"), "color": self.container.attr("color"), "tannins": self.container.attr("tannins"), "cool": self.container.attr("cool")}
        #TODO How to get the wanted values?
        self.wantedValues = {}
