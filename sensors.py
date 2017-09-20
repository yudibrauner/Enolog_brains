from container import *
from random import randint, randrange, uniform  # uniform=for float range
import threading

SENSORS_INTERVAL = 5


class Sensors:
    def __init__(self, container, generator, file):
        self.container = container
        self.generator = generator
        self.tannin = 0
        self.color = 0
        self.density = 0
        self.temperature = 0
        self.SENSORS = (self.tannin, self.color, self.density, self.temperature)
        self.file = file
        self.sensors_thread = None
        # self.startReading()

    # This method is run by the data generator after first data is written to the container
    def startReading(self):
        self.sensors_thread = threading.Thread(target=self.readData, daemon=True)
        self.sensors_thread.start()

    def readData(self):
        while self.generator.stay_alive:
            self.tannin = self.container.tannins.get()
            print('self.container.tannins.get(): ' + self.container.tannins.get())
            self.color = self.container.color.get()
            self.density = self.container.density.get()
            self.temperature = self.container.temperature.get()
            self.addSensorError()
            self.writeData()
            time.sleep(SENSORS_INTERVAL)  # Read data every SENSORS_INTERVAL seconds

    def addSensorError(self):
        numOfSensors = 3
        threshold = 1
        dataValues = list()
        for sensor in self.SENSORS:
            if sensor == self.density or sensor == self.tannin:
                threshold = 10
            for i in range(numOfSensors):
                rand1 = randrange(1, 101)
                print(sensor)
                if rand1 < 90:
                    tempThresh = round(random.uniform(0, threshold), 2)
                    print('tempThresh: ' + str(tempThresh))
                else:
                    tempThresh = round(random.uniform(0, threshold*1.1), 2)
                    print('tempThresh: ' + str(tempThresh))
                rand2 = random.randint(0, 1)
                if rand2 == 0:
                    dataValues.append(sensor - tempThresh)
                else:
                    dataValues.append(sensor + tempThresh)
            print(' dataValues: ' + str(dataValues))
            sensor = round(sum(dataValues) / float(len(dataValues)), 2)
            print('final average:' + str(sensor))
            # time.sleep(SENSORS_INTERVAL)

    def writeData(self):
        new_line = str(self.generator.run_time) + ' ' + str(self.tannin) + ' ' + str(self.color) + ' ' + str(self.density) + ' ' + str(self.temperature)
        with open(self.file, 'a') as write_file:
            write_file.write(new_line + '\n')




