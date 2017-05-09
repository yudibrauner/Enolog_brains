# -*- coding: utf-8 -*-
from container import *
from allContainers import *
from task import *
from winery import *


def print_menu():
    print('=====================')
    print('Menu:')
    print('q - quit')
    print('m - menu')
    print('p - print container list')
    print('1 - start container')
    print('2 - add task to container')
    print('3 - remove container')
    print('4 - move robotic arm')
    print('5 - set robotic arms home position')
    print('6 - start winery')
    print('=====================')


def addCont():
    # gets name and adds container
    num = input('container ID number in winery: ')
    # Todo: check if ID number is valid (from winery.allContainers)
    name = input('name (wine type): ')
    init_priority = input('initial priority: ')
    container = Container(name, num, init_priority)
    containers.addNewContainer(container)
    print('-> container added')


def addTaskToContainer():
    # gets num of container and adds a new task
    containers.printContainersList()
    num = input('container number in winery: ')
    Task.printAllTasks()
    tsk = input('input task: ')
    cont = containers.getContainer(num)
    cont.addTask(tsk)


def removeCont():
    # gets name and removes container
    name = input('name: ')
    success = containers.removeContainer(name)
    if success:
        print('-> container has been removed')


def moveRoboticArm():
    x, y, z = robArm.getPosition()
    print('current location:  X=' + str(x) + ' Y=' + str(y) + ' Z=' + str(z))
    dir = input('Direction? (N=north, E=east, S=south, W=west, U=up, D=down)')
    steps = input('Steps? ' + 'X:(0-' + str(robArm.xBoundaries-1) + ')' + ' Y:(0-' + str(robArm.yBoundaries-1) + ')' + ' Z:(0-' + str(robArm.zBoundaries-1) + ')')
    moved = robArm.move(dir, steps)
    x, y, z = robArm.getPosition()
    if moved:
        print('robot moved to:  X=' + str(x) + ' Y=' + str(y) + ' Z=' + str(z))
    else:
        print('-> out of bounds try again')
        moveRoboticArm()


def setHomePosition():
    x, y, z = robArm.getPosition()
    print('current location:  X=' + str(x) + ' Y=' + str(y) + ' Z=' + str(z))
    robArm.setHomePosition()
    print('-> setting home position to current location...')
    x, y, z = robArm.home.get()
    print('home position set to:  X=' + str(x) + ' Y=' + str(y) + ' Z=' + str(z))


def startWinery():
    winery = Winery()


def case(inp):
    if inp == 'm':
        print_menu()
    elif inp == 'p':
        containers.printFullList()
    elif inp == '1':
        addCont()
    elif inp == '2':
        addTaskToContainer()
    elif inp == '3':
        removeCont()
    elif inp == '4':
        moveRoboticArm()
    elif inp == '5':
        setHomePosition()
    elif inp == '6':
        startWinery()
    else:
        print('-> Wrong input try again')


# --------------------------------------------------------------------------------------------------------
containers = AllContainers()

if __name__ == '__main__':
    robArm = RoboticArm()
    print_menu()
    while True:
        inp = input('Input: ')
        if inp == 'q':
            break
        else:
            case(inp)

    containers.printFullList()
