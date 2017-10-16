# This class makes the data instead of the real containers

import datetime
import os
from random import randint, randrange, uniform  # uniform=for float range
import time
from container import *

THRESHOLD = 2
PROPORSION = 12

class DataGenerator:
    def __init__(self, container, file, program, program_files, interval, logger):
        self.container = container
        self.wine_name = self.container.name.get()
        self.file = file
        self.program = program
        self.tannins_file, self.color_file, self.density_file, self.cool_file, self.temperature_file, self.pump_file = program_files
        self.stay_alive = True
        self.interval = float(interval)
        self.logger = logger
        self.cool_list = list()
        self.density_list = list()
        self.color_list = list()
        self.tannins_list = list()
        self.temperature_list = list()
        self.pump_list = list()
        self.attrNames = self.container.listsAndDicts['attrNames']
        self.lists = {}
        self.thresholds = {"tannins": 1.2, "color": 0.025, "density": 1.5, "cool": 0.085, "temperature": 0.1}
        self.files = {'tannins': self.tannins_file, 'color': self.color_file, 'density': self.density_file,
                      'temperature': self.temperature_file, 'cool': self.cool_file, 'pump': self.pump_file}
        self.dictParams = {}
        self.sensorNames = self.container.listsAndDicts['sensorNames']
        self.heights = self.container.listsAndDicts['heights']
        for sensorName in self.sensorNames:
            self.dictParams[sensorName] = {}
            for height in self.heights:
                self.dictParams[sensorName][height] = -404
        for attrName in self.attrNames:
            self.lists[attrName] = list()
        self.run_time = -1
        self.isFirstRound = True

    def start_generating(self):
        new_line = '0 5 1 1110 0.5 18 1'  # time tannins color density cool temp pump
        self.createDataLists()
        self.createDataLists2()
        self.maxRun = len(self.lists['color']) - 1
        while self.stay_alive:
            self.run_time += 1
            with open(self.file, 'a') as write_file:
                write_file.write(new_line + '\n')
                prev_line = new_line
                new_line = self.generate_new_line(prev_line)
                if self.run_time >= self.maxRun:
                    self.stay_alive = False
            time.sleep(float(self.interval))
        self.container.fermIsFinished()

    def createDataLists(self):
        for (file, lst) in zip([self.tannins_file, self.color_file, self.density_file, self.cool_file, self.temperature_file, self.pump_file],
                               [self.tannins_list, self.color_list, self.density_list, self.cool_list, self.temperature_list, self.pump_list]):
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

    def createDataLists2(self):
        for (file, lst) in zip([self.files['tannins'], self.files['color'], self.files['density'], self.files['cool'], self.files['temperature'], self.files['pump']],
                               [self.lists['tannins'], self.lists['color'], self.lists['density'], self.lists['cool'], self.lists['temperature'], self.lists['pump']]):
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

    def set_expected_attrs(self):
        for attrName in self.attrNames:
            expected_curr = self.lists[attrName][self.run_time]
            self.container.setExpectedValue(attrName, round(expected_curr, 3))

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
        expected_curr = lst[self.run_time]
        expected_prev = lst[self.run_time - 1]
        if self.run_time == 0:
            expected_prev = prev
        expected_dist = expected_curr - expected_prev
        if expected_dist == 0:
            expected_dist = round(random.uniform(-0.1, 0.1), 2)
        return round(prev + expected_dist + self.getNewDelta(expected_dist), 2)

    def generateNewValue2(self, prev, sensorName):
        expected_curr = self.lists[sensorName][self.run_time]
        expected_prev = self.lists[sensorName][self.run_time - 1]
        if self.run_time == 0:
            expected_prev = prev
        expected_dist = expected_curr - expected_prev
        if expected_dist == 0:
            expected_dist = round(random.uniform(-self.thresholds[sensorName], self.thresholds[sensorName]), 2)
        return round(prev + expected_dist + self.getNewDelta(expected_dist), 2)

    def generateNewTemp(self, lst):
        if self.run_time == len(lst): # For avoiding exceptions of out of index
            return "end"
        expected_curr = self.container.getDefTemp()
        dist = lst[self.run_time]
        randPercent = randrange(1, 101)
        randPositivity = random.randint(0, 1)
        plus = 0.1
        if randPositivity == 0:
            plus *= -1
        if randPercent < 90:
            value = expected_curr + 0.1 * dist
        elif randPercent < 96:
            value = expected_curr + 0.1 * dist + plus
        else:
            value = expected_curr + 0.1 * dist + plus * 2
        return round(value, 2)

    def generate_new_line(self, prev_line):
        parts = prev_line.split(' ')
        prev_tannins, prev_color, prev_density, prev_cool, prev_temperature, prev_pump = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5]), float(parts[6])
        self.set_expected_attrs()
        curr_tannins2 = self.generateNewValue2(prev_tannins, 'tannins')
        curr_color2 = self.generateNewValue2(prev_color, 'color')
        curr_density2 = self.generateNewValue2(prev_density, 'density')
        curr_temperature2 = self.generateNewValue2(prev_temperature, 'temperature')
        curr_temperature2 = self.lists['temperature'][self.run_time]
        curr_pump = 0
        curr_cool = 0
        curr_temp = self.generateNewTemp(self.cool_list)
        new_line = str(self.run_time) + ' ' + str(curr_tannins2) + ' ' + str(curr_color2) + ' ' + str(curr_density2) + ' '\
                   + str(curr_cool) + ' ' + str(curr_temperature2) + ' ' + str(curr_pump)
        self.container.setDateTime(datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S"))
        self.setNewValues(curr_temperature2, curr_tannins2, curr_color2, curr_density2)
        if self.isFirstRound:  # starts sensors reading - only after first data is written
            self.container.sensors.startReading()
            self.isFirstRound = False
        return new_line

    def getMatchHeight(self, value, sensorName, Height):
        if Height == 'bot':
            return value
        if sensorName == 'color' or sensorName == 'tannins':
            delta = random.uniform(0, self.thresholds[sensorName])
            posOrNeg = random.randint(0, 1)
            if posOrNeg == 1:
                delta *= (-1)
        elif sensorName == 'density':
            if Height == 'mid':
                delta = random.uniform(0, self.thresholds[sensorName])
            else:
                delta = random.uniform(self.thresholds[sensorName], 2*self.thresholds[sensorName])
            delta *= (-1)
        else:
            if Height == 'mid':
                delta = random.uniform(0, 2*self.thresholds[sensorName])
            else:
                delta = random.uniform(1.5*self.thresholds[sensorName], 4*self.thresholds[sensorName])
        return value + delta

    def setNewValues(self, botTemperature, botTannins, botColor, botDensity):
        # for the cooler will cool the temp
        botTemperature += 0.5 * float(self.lists['cool'][self.run_time])

        values = {'temperature': botTemperature,'tannins': botTannins, 'density': botDensity, 'color': botColor}
        for sensorName in self.sensorNames:
            for height in self.heights:
                self.dictParams[sensorName][height] = self.getMatchHeight(values[sensorName], sensorName, height)
        for sensorName in self.sensorNames:
            for height in self.heights:
                self.container.setRealValues(sensorName, height, self.dictParams[sensorName][height])

    def prettyNewLine(self, new_line):
        parsed = str(new_line).split(' ')
        return 'Time: ' + parsed[0] + ' Tannins:' + parsed[1] + ' Color: ' + parsed[2] + ' Density: ' + parsed[3] +\
               ' Cool: ' + parsed[4] + ' Temperature: ' + parsed[5] + ' Pump: ' + parsed[6]

    def setInterval(self, interval):
        self.interval = interval

    def updateLogger(self, logger):
        self.logger = logger