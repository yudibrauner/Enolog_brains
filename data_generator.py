import os
from random import randint, randrange, uniform  # uniform=for float range
import time
from container import *

# TANNINS_FAST =
# TANNINS_NORMAL =
# TANNINS_SLOW =
# TEMPERATURE_FAST =
# TEMPERATURE_NORMAL =
# TEMPERATURE_SLOW =
# COLOR_FAST =
# COLOR_NORMAL =
# COLOR_SLOW =
# DENSITY_FAST =
# DENSITY_NORMAL =
# DENSITY_SLOW =


class DataGenerator:
    def __init__(self, container, file, program_files, interval, logger):
        self.container = container
        self.file = file
        self.tannin, self.color, self.density, self.temperature = program_files
        self.stay_alive = True
        self.interval = float(interval)
        self.logger = logger

    def generate_new_line(self, prev_line):
        parts = prev_line.split(' ')
        tannins = (int(parts[1]) + randrange(0, 5))
        color = (round(float((float(parts[2])) + random.random()), 1))
        density = (int(parts[3]) + randrange(-15, 0))
        temperature = (int(parts[1]) + randrange(0, 2))
        new_time = float(parts[0]) + float(self.interval)
        # print('new_time: ' + str(new_time))
        new_line = str(new_time) + ' ' + str(tannins) + ' ' + str(color) + ' ' + str(density) + ' ' + str(temperature)
        self.container.setTemperature(temperature)
        self.container.setTannin(tannins)
        self.container.setColor(color)
        self.container.setDensity(density)
        # self.container.decider.setNewData(new_time, tannins, color, density, temperature)
        return new_line

    def start_generating(self):
        new_line = '0 5 1 1110 0.5'  # time tannins color density temperature
        while self.stay_alive:
            with open(self.file, 'a') as write_file:
                write_file.write(new_line + '\n')
                self.logger.info(self.prettyNewLine(new_line))
                prev_line = new_line
                new_line = self.generate_new_line(prev_line)
            # print(str(self.interval))
            time.sleep(float(self.interval))

    def prettyNewLine(self, new_line):
        parsed = str(new_line).split(' ')
        return 'Time: ' + parsed[0] + ' Tannins:' + parsed[1] + ' Color: ' + parsed[2] + ' Density: ' + parsed[3] + ' Temperature: ' + parsed[3]

    def setInterval(self, inteval):
        self.interval = inteval

    def updateLogger(self, logger):
        self.logger = logger

