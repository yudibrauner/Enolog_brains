# This is the robotic arm class
import armTask


class RoboticArm:
    def __init__(self):
        self.status = 0               # 0-free | 1-moving | 2-working

    @staticmethod
    def stir(self):
        print('the arm is stirring')

    @staticmethod
    def getColor(self):
        print('the arm is getting the wine color')

