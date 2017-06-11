from container import *
from data_generator import  *


class Decider:

    def __init__(self, fermentation, fermentation_file):
        self.fermentation_program = fermentation
        self.fermentation_file = fermentation_file
        self.times = list()
        self.tannins = list()
        self.color = list()
        self.density = list()
        self.temperature = list()

    def setNewData(self, new_time, tannins, color, density, temperature):
        self.times.append(new_time)
        self.tannins.append(tannins)
        self.color.append(color)
        self.density.append(density)
        self.temperature.append(temperature)
        self.calculateTrend()

    def calculateTrend(self):
        # TODO: calculate trend from new data and from expected data and compare
        # https://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
        # https://www.mathworks.com/help/matlab/ref/polyfit.html
        print('does nothing at the moment')



