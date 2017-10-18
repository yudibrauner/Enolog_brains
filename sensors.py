from container import *
from random import randint, randrange, uniform  # uniform=for float range
import threading
import math
from decider import *
import random


class Sensors:
    def __init__(self, container, logger):#, generator, file):
        self.container = container
        self.generator = container.generator
        self.logger = logger
        self.sensorsNames = ["tannins", "color", "density", "temperature"]
        self.sensorsHeights = ['top', 'mid', 'bot']
        self.dictSensors = {"tannins": {'top': 0, 'mid': 0, 'bot': 0}, "color": {'top': 0, 'mid': 0, 'bot': 0},
                            "density": {'top': 0, 'mid': 0, 'bot': 0}, "temperature": {'top': 0, 'mid': 0, 'bot': 0}, "cool": 0, 'pump': 0}
        self.thresholds = {"tannins": 1.2, "color": 0.025, "density": 1.5, "cool": 0.085, "temperature":0.1}
        self.sensorsInterval = container.sensorsInterval
        self.numOfSensors = container.numOfSensors
        self.file = container.sensors_data
        self.sensors_thread = None
        self.decider = Decider(container)

    # This method is run by the data generator after first data is written to the container
    def startReading(self):
        self.sensors_thread = threading.Thread(target=self.readDataLoop, daemon=True)
        self.sensors_thread.start()

    def readDataLoop(self):
        self.sensorsInterval = self.container.sensorsInterval
        while self.generator.stay_alive:
            self.container.hoursFromStart.set(float(self.container.hoursFromStart.get()) + 0.5)
            self.container.add2matrix()
            self.readData()
            time.sleep(self.sensorsInterval)  # Read data every SENSORS_INTERVAL seconds

    def sense(self):
        print("not important")

    def readData(self):
        for sensorName in self.sensorsNames:
            self.dictSensors[sensorName] = self.addSensorNewError(sensorName)
        self.writeData()

    # This function takes a value and a threshold and creates X values, deletes the farthest value, and returns the average of the others.
    def addSensorError(self, sensor):
        value = self.container.attr(sensor)
        threshold = self.thresholds[sensor]
        numOfSensors = self.numOfSensors
        values = []
        for i in range(numOfSensors):
            newValue = self.createTheError(value, threshold)
            values.append(newValue)
        averageSensors = sum(values) / float(numOfSensors)
        indexOfFarest = 0
        farest = math.fabs(values[indexOfFarest] - averageSensors)
        for i in range(numOfSensors):
            curValue = math.fabs(values[i] - averageSensors)
            if curValue > farest:
                farest = curValue
                indexOfFarest = i
        del values[indexOfFarest]
        averageSensors = round(sum(values) / float(numOfSensors - 1), 2)
        return averageSensors

    def createTheError(self, value, threshold):
        value = float(value)
        outValue = value
        randOfBigError = randrange(1, 101)
        if randOfBigError < 99:  # most of the times there won't be a mistake
            deviation = round(random.uniform(0, threshold), 2)
        else:
            deviation = round(random.uniform(0, threshold * 40), 2)
        randOfPositivity = random.randint(0, 1)
        if randOfPositivity == 0:
            outValue = value - deviation
        else:
            outValue = value + deviation
        return outValue

    def addSensorError2(self, sensor, value):
        threshold = self.thresholds[sensor]
        numOfSensors = self.numOfSensors
        values = []
        for i in range(numOfSensors):
            newValue = self.createTheError(value, threshold)
            values.append(newValue)
        averageSensors = sum(values) / float(numOfSensors)
        indexOfFarest = 0
        farest = math.fabs(values[indexOfFarest] - averageSensors)
        for i in range(numOfSensors):
            curValue = math.fabs(values[i] - averageSensors)
            if curValue > farest:
                farest = curValue
                indexOfFarest = i
        del values[indexOfFarest]
        averageSensors = round(sum(values) / float(numOfSensors - 1), 2)
        return averageSensors

    # this is the function that works. it's without threshold, take from this^
    def addSensorNewError(self, sensor):
        # averageSensors = self.sensors[sensor]
        in_top = float(self.container.getRealAttr(sensor, 'top'))
        in_mid = float(self.container.getRealAttr(sensor, 'mid'))
        in_bot = float(self.container.getRealAttr(sensor, 'bot'))
        out_top = round(self.addSensorError2(sensor, in_top), 2)
        out_mid = round(self.addSensorError2(sensor, in_mid), 2)
        out_bot = round(self.addSensorError2(sensor, in_bot), 2)
        return {'top': out_top, 'mid': out_mid, 'bot': out_bot}

    def writeData(self):
        for sensorName in self.sensorsNames:
            for height in self.sensorsHeights:
                self.container.setSenseValue(sensorName, height, self.dictSensors[sensorName][height])
        self.pumpAndCool()
        self.dictSensors['pump'] = self.container.get_SenseAttr('pump', 0)
        self.dictSensors['cool'] = self.container.get_SenseAttr('cool', 0)
        new_line = str(self.generator.run_time) + ' ' + str(self.dictSensors['tannins']['top']) + ' ' + str(
            self.dictSensors['color']['top']) + ' ' + str(self.dictSensors['density']['top']) + ' ' + str(self.dictSensors['cool']) + ' ' + str(
            self.dictSensors['temperature']['top']) + ' ' + str(self.dictSensors['pump'])
        with open(self.file, 'a') as write_file:
            write_file.write(new_line + '\n')
        self.logger.info('[' + str(self.container.id) + '] ' + str(self.container.name.get()) + ' ' + new_line)
        self.decider.decide()

    def pumpAndCool(self):
        self.container.checkCool()
        self.container.checkPump(int(float(self.container.get_ExpectedAttr('pump'))))
        self.container.setCoolSum()
        self.container.setPumpSum()

    def setSensorsInterval(self):
        self.sensorsInterval = self.container.sensorsInterval