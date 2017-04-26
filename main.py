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
    name = input('name: ')
    container = Container(name)
    containers.addNewContainer(container)
    print('adding container...')

def removeCont():
    # gets name and adds container
    name = input('name: ')
    containers.removeContainer(name)
    print('removing container...')


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
