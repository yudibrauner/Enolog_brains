# The winery class manages the locations of all the containers and creates a map of the winery


class Winery:
    def __init__(self, name):
        self.name = name
        self.allWineryContainers = dict()
        self.numOfWineryContainers = 0

    class WineryContainer:
        def __init__(self, num, x, y, z, maxCapacity):
            self.num = num
            self.x = x
            self.y = y
            self.z = z
            self.maxCapacity = maxCapacity

    def addContainerToWinery(self, wineryContainer):
        self.allWineryContainers[wineryContainer.num] = wineryContainer
        self.numOfWineryContainers += 1

    def removeContainerFromWinery(self, num):
        self.allWineryContainers.pop(num)
        self.numOfWineryContainers -= 1

    # TODO: make the winery into a file and read container info from file
    def getWineryContainerLocation(self, num):
        x = self.allWineryContainers[num].x
        y = self.allWineryContainers[num].y
        z = self.allWineryContainers[num].z
        return x, y, z


