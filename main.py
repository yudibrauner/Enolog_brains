from container import *
from allContainers import *


def print_menu():
    print('=====================')
    print('Menu:')
    print('q - quit')
    print('m - menu')
    print('p - print container list')
    print('1 - add container')
    print('2 - remove container')
    print('=====================')


def addCont():
    # gets name and adds container
    num = input('container number in winery: ')
    name = input('name: ')
    init_priority = input('initial priority: ')
    container = Container(name, num, init_priority)
    containers.addNewContainer(container)
    print('-> container added')


def removeCont():
    # gets name and removes container
    name = input('name: ')
    success = containers.removeContainer(name)
    if success:
        print('-> container has been removed')


def case(inp):
    if inp == 'm':
        print_menu()
    elif inp == 'p':
        containers.printList()
    elif inp == '1':
        addCont()
    elif inp == '2':
        removeCont()


containers = AllContainers()

if __name__ == '__main__':
    print_menu()
    while True:
        inp = input()
        if inp == 'q':
            break
        else:
            case(inp)
    '''
    numOfContainers = int(input('How many containers?\n'))

    for i in range(numOfContainers):
        print('\nContainer ' + str(i) + ':')
        name = input('Name:')
        cntnr = Container(name)
        containers.addNewContainer(cntnr)
    '''
    containers.printList()
