from container import *
from random import randint, randrange, uniform  # uniform=for float range
import threading
import math
from decider import *


class Sensors:
    def __init__(self, container):#, generator, file):
        self.container = container
        self.generator = container.generator
        self.sensorsNames = ["tannins", "color", "density", "cool", "temperature"]
        self.sensors = {"tannins": 0, "color": 0, "density": 0, "cool": 0, "temperature":0}
        # the thresholds now are one percent of the distance between the max value and min value of the attribute, TODO: think of that thresholds
        self.thresholds = {"tannins": 0.75, "color": 0.025, "density": 1.15, "cool": 0.085, "temperature":0}
        self.sensorsInterval = container.sensorsInterval
        self.numOfSensors = container.numOfSensors
        self.file = container.sensors_data
        self.sensors_thread = None
        self.decider = Decider(container)

    # This method is run by the data generator after first data is written to the container
    def startReading(self):
        self.sensors_thread = threading.Thread(target=self.readData, daemon=True)
        self.sensors_thread.start()

    def readData(self):
        self.sensorsInterval = self.container.sensorsInterval
        while self.generator.stay_alive:
            for sensorName in self.sensorsNames:
                if sensorName == "temperature":
                    self.sensors[sensorName] = self.container.attr(sensorName)
                elif sensorName == "cool":
                    self.container.setCool(0)
                else:
                    self.sensors[sensorName] = self.addSensorError(sensorName)
            self.writeData()
            time.sleep(self.sensorsInterval)  # Read data every SENSORS_INTERVAL seconds

    # This function takes a value and a threshold and creates X values, deletes the farest value, and returns the average of the others.
    def addSensorError(self, sensor):
        value = self.container.attr(sensor)
        threshold = self.thresholds[sensor]
        numOfSensors = self.numOfSensors
        values = []
        for i in range(numOfSensors):
            newValue = self.createTheError(value, threshold)
            values.append(newValue)
        # print('the real ' + sensor + ' is ' + value + '. the sensors get' + str(values))
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
        # print('the remain sensors get' + str(values) + '. the average is ' + str(averageSensors))
        return averageSensors

    def createTheError(self, value, threshold):
        value = float(value)
        outValue = value
        randOfBigError = randrange(1, 101)
        if randOfBigError < 99:  # most of the times there won't be a mistake
            deviation = round(random.uniform(0, threshold), 2)
            # deviation = 0
        else:
            deviation = round(random.uniform(0, threshold * 40), 2)
            # deviation = 0
        randOfPositivity = random.randint(0, 1)
        if randOfPositivity == 0:
            outValue = value - deviation
        else:
            outValue = value + deviation
        return outValue

    def writeData(self):
        new_line = str(self.generator.run_time) + ' ' + str(self.sensors['tannins']) + ' ' + str(self.sensors['color']) + ' ' + str(self.sensors['density']) + ' ' + str(self.sensors['cool'])
        # print('tannins:' + str(self.sensors['tannins']) + ', color:' + str(self.sensors['color']) + ', dens:' + str(self.sensors['density']) + ', temp:' + str(self.sensors['cool']))
        for sensorName in self.sensorsNames:
            self.container.setRealValue(sensorName, self.sensors[sensorName])
        with open(self.file, 'a') as write_file:
            write_file.write(new_line + '\n')
        self.container.checkTemp()
        self.decider.decide()