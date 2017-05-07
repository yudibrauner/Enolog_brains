# The winery class manages the locations of all the containers and creates a map of the winery
import os.path


class Winery:
    def __init__(self):
        self.name = None
        self.winery_x = 100
        self.winery_y = 100
        self.winery_z = 10
        self.allWineryContainers = dict()
        self.numOfWineryContainers = 0
        self.fileName = 'winery.txt'
        if not os.path.exists(self.fileName):
            self.initFile()
        else:
            self.readFromFile()


    class WineryContainer:
        def __init__(self, num, x, y, z, maxCapacity=100):
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

    def getWineryContainerLocation(self, num):
        x = self.allWineryContainers[num].x
        y = self.allWineryContainers[num].y
        z = self.allWineryContainers[num].z
        return x, y, z

    def initFile(self):
        self.name = input('Enter Winery name: ')
        self.winery_x = input('Set winery width (x dimensions): ')
        self.winery_y = input('Set winery length (y dimensions): ')
        self.winery_z = input('Set winery length (z dimensions): ')
        numOfContainers = input('Enter number of winery containers: ')
        for i in range(int(numOfContainers)):
            print('Container #' + str(i+1) + ':')
            num = input('Enter serial number: ')
            x = input('Enter container X location: ')
            y = input('Enter container Y location: ')
            z = input('Enter container Z location (container height): ')
            container = self.WineryContainer(num, x, y, z)
            self.addContainerToWinery(container)
        with open(self.fileName, 'a') as file:
            file.write('======================================================' + '\n')
            file.write('              Winery: ' + str(self.name) + '\n')
            file.write('======================================================' + '\n')
            file.write('Dimensions:  (Width Length Height) \n')
            file.write(self.winery_x + ' ' + self.winery_y + ' ' + self.winery_z + '\n')
            file.write('Containers:' + '\n')
            for container_num, container in self.allWineryContainers.items():
                file.write(container_num + ' ' + container.x + ' ' + container.y + ' ' + container.z + '\n')

    def readFromFile(self):
        useExistingFile = input('Would you like to use existing winery? (y/n)') # TODO add name of winery from file to question
        while not useExistingFile == 'y' and not useExistingFile == 'n':
            print('-> ERROR: bad input try again')
            useExistingFile = input('Would you like to use existing winery? (y/n)') # ^here to^
        if useExistingFile == 'n':
            os.remove(self.fileName)
            self.initFile()
        elif useExistingFile == 'y':
            print('READING DATA FROM EXISTING FILE')  # TODO read data from file and set the class params
