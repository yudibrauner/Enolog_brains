# This is the robotic arm class
# CLIENT
import task


class RoboticArm:
    def __init__(self):
        self.status = 0               # 0-free | 1-moving | 2-working
        self.home = self.HomePosition()
        self.xLocation = self.home.x
        self.yLocation = self.home.y
        self.zLocation = self.home.z
        self.xBoundaries = 101       # the actual range is 0-100
        self.yBoundaries = 101
        self.zBoundaries = 11

    class HomePosition:
        """
        This is the Robotic Arm's home position Class
        """
        def __init__(self):
            self.x = 0
            self.y = 0
            self.z = 0

        def set(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

        def get(self):
            return self.x, self.y, self.z

    def setHomePosition(self):
        self.home.set(self.xLocation, self.yLocation, self.zLocation)

    def move(self, direction, steps):
        """
        :param direction: N=north, E=east, S=south, W=west, U=up, D=down
        :param steps: all positive Natural numbers
        :return: void
        """
        moved = False
        steps = int(steps)
        if direction == 'N':
            if self.yLocation + steps in range(self.yBoundaries):
                self.yLocation += steps
                moved = True
        elif direction == 'S':
            if self.yLocation - steps in range(self.yBoundaries):
                self.yLocation -= steps
                moved = True
        elif direction == 'E':
            if self.xLocation + steps in range(self.xBoundaries):
                self.xLocation += steps
                moved = True
        elif direction == 'W':
            if self.xLocation - steps in range(self.xBoundaries):
                self.xLocation -= steps
                moved = True
        elif direction == 'U':
            if self.zLocation + steps in range(self.zBoundaries):
                self.zLocation += steps
                moved = True
        elif direction == 'D':
            if self.zLocation - steps in range(self.zBoundaries):
                self.zLocation -= steps
                moved = True
        return moved


    def getPosition(self):
        return self.xLocation, self.yLocation, self.zLocation

    @staticmethod
    def stir():
        print('the arm is stirring')

    @staticmethod
    def getColor():
        print('the arm is getting wine color')

