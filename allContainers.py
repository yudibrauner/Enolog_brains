# This class holds all the current containers

class AllContainers:

    def __init__(self):
        self.numOfContainers = 0
        self.listOfContainers = list()

    def addNewContainer(self, container):
        self.listOfContainers.append(container)
        self.numOfContainers += 1

    def removeContainer(self, container_name):
        for cntnr in self.listOfContainers:
            if cntnr.name == container_name:
                self.listOfContainers.remove(cntnr)
        self.numOfContainers -= 1

    def printList(self):
        print('--------------------------------')
        print('PRINTING LIST OF CONTAINERS: (' + str(self.numOfContainers) + ')')
        print('--------------------------------')
        for i, cntnr in enumerate(self.listOfContainers):
            print('\n' + str(i+1) + '.')
            cntnr.printContainer()

