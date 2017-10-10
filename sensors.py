from container import *
from random import randint, randrange, uniform  # uniform=for float range
import threading
import math
from decider import *


class Sensors:
    def __init__(self, container, logger):#, generator, file):
        self.container = container
        self.generator = container.generator
        self.logger = logger
        self.sensorsNames = ["tannins", "color", "density", "cool", "temperature"]
        self.sensorsHeights = ['top', 'mid', 'bot']
        self.sensors = {"tannins": 0, "color": 0, "density": 0, "cool": 0, "temperature":0}
        self.dictSensors = {"tannins": {'top': 0, 'mid': 0, 'bot': 0}, "color": {'top': 0, 'mid': 0, 'bot': 0},
                            "density": {'top': 0, 'mid': 0, 'bot': 0}, "temperature": {'top': 0, 'mid': 0, 'bot': 0}, "cool": 0, 'pump': 0}
        # the thresholds now are one percent of the distance between the max value and min value of the attribute, TODO: think of that thresholds
        self.thresholds = {"tannins": 1.2, "color": 0.025, "density": 1.5, "cool": 0.085, "temperature":0}
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
            self.container.howersFromStart.set(float(self.container.howersFromStart.get()) + 0.5)
            self.container.add2matrix()
            self.readData()
            time.sleep(self.sensorsInterval)  # Read data every SENSORS_INTERVAL seconds

    def readData(self):
        for sensorName in self.sensorsNames:
            if sensorName == "temperature":
                self.sensors[sensorName] = self.container.attr(sensorName)
                self.dictSensors[sensorName] = self.addSensorNewError(sensorName)
            elif sensorName == "cool":
                self.container.setCool(0)
            else:
                self.sensors[sensorName] = self.addSensorError(sensorName)
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

    def addSensorNewError(self, sensor):
        averageSensors = self.sensors[sensor]
        top = round(float(self.container.getRealAttr(sensor, 'top')), 2)
        mid = round(float(self.container.getRealAttr(sensor, 'mid')), 2)
        bot = round(float(self.container.getRealAttr(sensor, 'bot')), 2)
        return {'top': top, 'mid': mid, 'bot': bot}

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

    def writeData(self):
        curCool = str(self.container.attr("cool"))
        # if curCool == "N/A":
        #     curCool = "0"
        new_line = str(self.generator.run_time) + ' ' + str(self.sensors['tannins']) + ' ' + str(self.sensors['color']) + ' ' + str(self.sensors['density']) + ' ' + curCool
        # print('tannins:' + str(self.sensors['tannins']) + ', color:' + str(self.sensors['color']) + ', dens:' + str(self.sensors['density']) + ', temp:' + str(self.sensors['cool']))
        for sensorName in self.sensorsNames:
            self.container.setRealValue(sensorName, self.sensors[sensorName])
            if sensorName != 'cool' and sensorName != 'pump':
                for height in self.sensorsHeights:
                    self.container.setSenseValue(sensorName, height, self.dictSensors[sensorName][height])
        # self.container.setRealValueDict('cool', 'center', self.sensors['cool'])
        # self.container.setRealValueDict('pump', 'center', self.dictSensors['pump'])
        self.container.checkTemp()
        with open(self.file, 'a') as write_file:
            write_file.write(new_line + '\n')
        self.logger.info('[' + str(self.container.id) + '] ' + str(self.container.name.get()) + ' ' + new_line)
        self.pumpAndCool()
        self.decider.decide()

    def pumpAndCool(self):
        self.container.checkCool()
        self.container.checkPump(int(float(self.container.get_ExpectedAttr('pump'))))
        self.container.setCoolSum()
        self.container.setPumpSum()

    def setSensorsInterval(self):
        self.sensorsInterval = self.container.sensorsInterval