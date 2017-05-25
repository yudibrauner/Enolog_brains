import os
from random import randint, randrange, uniform  # uniform=for float range
import time


class DataGenerator:
    def __init__(self, file, program_files):
        self.file = file
        self.tannin, self.color, self.density, self.temperature = program_files
        self.start_generating()

    def generate_new_line(self, line):
        parts = line.split(' ')
        new_line = parts[0]  # time
        new_line += ' ' + str(int(parts[1]) + randrange(-2, 2))
        return new_line

    def start_generating(self):
        with open(self.file, 'w') as write_file:
            with open(self.tannin, 'r') as read_file:
                lines = read_file.readlines()
                for i in range(len(lines)+1):
                    last_line = lines[-i]
                    new_line = self.generate_new_line(last_line)
                    write_file.write(new_line + '\n')



