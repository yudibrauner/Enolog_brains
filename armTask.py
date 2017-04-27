# This class is a mission for the robotic arm
from roboticArm import *


TYPES = {'stirr': RoboticArm.stir(),
         'color': RoboticArm.getColor()}


class ArmTask:
    def __init__(self, taskType):
        self.type = TYPES[taskType]

