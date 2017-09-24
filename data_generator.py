# This class makes the data instead of the real containers

import os
from random import randint, randrange, uniform  # uniform=for float range
import time
from container import *

THRESHOLD = 1
PROPORSION = 12

class DataGenerator:
    def __init__(self, container, file, program, program_files, interval, logger):
        self.container = container
        self.wine_name = self.container.name.get()
        self.file = file
        self.program = program
        self.tannin, self.color, self.density, self.temperature = program_files
        self.stay_alive = True
        self.interval = float(interval)
        self.logger = logger
        self.temperature_list = list()
        self.density_list = list()
        self.color_list = list()
        self.tannin_list = list()
        self.run_time = -1
        self.isFirstRound = True

    def getNewDelta(self, expected_dist):
        rand1 = randrange(1, 101)
        if rand1 < 90:
            new_range = expected_dist * THRESHOLD
            new_delta = round(random.uniform(0, new_range), 2)
        elif rand1 < 96:
            new_range = expected_dist * THRESHOLD
            new_delta = expected_dist * 0.1 + round(random.uniform(0, new_range), 2)
        else:
            new_range = expected_dist * THRESHOLD
            new_delta = expected_dist * 0.2 + round(random.uniform(0, new_range), 2)
        rand3 = random.randint(0, 1)
        if rand3 == 0:
            return - new_delta
        else:
            return new_delta

    def generateNewValue(self, prev, lst):
        if self.run_time == len(lst): # For avoiding exceptions of out of index
            return "end"
        expected_curr = lst[self.run_time]
        expected_prev = lst[self.run_time - 1]
        if self.run_time == 0:
            expected_prev = prev
        expected_dist = expected_curr - expected_prev
        if expected_dist == 0:
            expected_dist = round(random.uniform(-0.1, 0.1), 2)
        return round(prev + expected_dist + self.getNewDelta(expected_dist), 2)

    def generate_new_line(self, prev_line):
        parts = prev_line.split(' ')
        prev_tannins, prev_color, prev_density, prev_temperature = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
        curr_tannins = self.generateNewValue(prev_tannins, self.tannin_list)
        curr_color = self.generateNewValue(prev_color, self.color_list)
        curr_density = self.generateNewValue(prev_density, self.density_list)
        curr_temperature = self.generateNewValue(prev_temperature, self.temperature_list)
        # new_time = float(parts[0]) + float(self.interval)
        # print('new_time: ' + str(new_time))
        if curr_color == "end":
            return "end"
        new_line = str(self.run_time) + ' ' + str(curr_tannins) + ' ' + str(curr_color) + ' ' + str(curr_density) + ' ' + str(curr_temperature)
        self.container.setDateTime(datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S"))
        self.container.setTemperature(curr_temperature)
        self.container.setTannins(curr_tannins)
        self.container.setColor(curr_color)
        self.container.setDensity(curr_density)
        if self.isFirstRound:  # starts sensors reading - only after first data is written
            self.container.sensors.startReading()
            self.isFirstRound = False
        # self.container.decider.setNewData(new_time, tannins, color, density, temperature)
        return new_line

    def createDataLists(self):
        for (file, lst) in zip([self.tannin, self.color, self.density, self.temperature], [self.tannin_list, self.color_list, self.density_list, self.temperature_list]):
            with open(file, 'r') as f:
                lines = f.readlines()
                prev = round(float(lines[0].split(' ')[-1]), 2)
                lst.append(prev)
                for line in lines[1:]:
                    curr = round(float(line.split(' ')[-1]), 2)
                    delta = curr - prev
                    minute_delta = delta / PROPORSION
                    for i in range(0, PROPORSION):
                        lst.append(prev + (i * minute_delta))
                    prev = curr

    def start_generating(self):
        new_line = '0 5 1 1110 0.5'  # time tannins color density temperature
        self.createDataLists()
        while self.stay_alive:
            self.run_time += 1
            with open(self.file, 'a') as write_file:
                write_file.write(new_line + '\n')
                self.logger.info('[' + str(self.container.id) + '] ' + str(self.wine_name) + ' ' + self.prettyNewLine(new_line))
                prev_line = new_line
                new_line = self.generate_new_line(prev_line)
                if new_line == "end":
                    self.stay_alive = False
            time.sleep(float(self.interval))
        self.container.fermIsFinished()

    def prettyNewLine(self, new_line):
        parsed = str(new_line).split(' ')
        return 'Time: ' + parsed[0] + ' Tannins:' + parsed[1] + ' Color: ' + parsed[2] + ' Density: ' + parsed[3] + ' Temperature: ' + parsed[4]

    def setInterval(self, interval):
        self.interval = interval

    def updateLogger(self, logger):
        self.logger = logger