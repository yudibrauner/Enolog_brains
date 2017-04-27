# This class holds all the current containers

class AllContainers:

    def __init__(self):
        self.numOfContainers = 0
        self.listOfContainers = dict()

    def addNewContainer(self, container):
        self.listOfContainers[container.number] = container
        self.numOfContainers += 1

    def removeContainer(self, container_name):
        exists = False
        for cntnr in self.listOfContainers:
            if cntnr.name == container_name:
                self.listOfContainers.remove(cntnr)
                exists = True
        self.numOfContainers -= 1
        if not exists:
            print('-> ERROR: invalid input')
        return exists

    def getContainer(self, num):
        return self.listOfContainers[num]

    def printContainersList(self):
        print('List of valid containers:')
        for key in self.listOfContainers:
            print(key)

    def printFullList(self):
        print('--------------------------------')
        print('PRINTING LIST OF CONTAINERS: (' + str(self.numOfContainers) + ')')
        print('--------------------------------')
        for key in self.listOfContainers:
            print('\n' + str(key) + ':')
            self.listOfContainers[key].printContainer()

