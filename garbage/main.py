# -*- coding: utf-8 -*-
import tkinter.messagebox
from tkinter.filedialog import *

from Simulator import Simulator
from allContainers import *
from container import *
from task import *

from garbage.winery import *

#intialize items:

robArm = RoboticArm()
winery = ""


#functions:

def openSim():
    sim = Simulator(robArm, containers, winery)

def openFile():
    adress = askopenfilename()

def saveFile():
    adress = asksaveasfilename()

def mesBox():
    tkinter.messagebox.showinfo("About Us:", "Yehuda Brauner\nElyashiv Miller")


def printCont():
    containers.printFullList()

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


def addCont2():
    name = ''
    def getText():
        name = e1.get()
    e1.pack()
    b = Button(root, text="Enter", width=10, command=getText)
    b.pack()
    print(name)

def addCont():
    # gets name and adds container
    num = input('container ID number in winery: ')
    # Todo: check if ID number is valid (from winery.allContainers)
    name = input('name (wine type): ')
    init_priority = input('initial priority: ')
    container = Container(name, num, init_priority)
    containers.addNewContainer(container)
    subMenu3.add_command(label=name, command=printCont)
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

# if __name__ == '__main__':
#     robArm = RoboticArm()
#     print_menu()
#     while True:
#         inp = input('Input: ')
#         if inp == 'q':
#             break
#         else:
#             case(inp)
#
#     containers.printFullList()






buttons = []


root = Tk()

topFrame = Frame(root, width=1000, height=500)
# bottomFrame = Frame()
topFrame.pack()
# bottomFrame.pack(side=BOTTOM)
global containerLabel
containerLabel=Label(root, text='winery app')
containerLabel.pack()

menu=Menu(root)
root.config(menu=menu)

subMenu1 = Menu(menu)
menu.add_cascade(label="file", menu=subMenu1)
subMenu1.add_command(label="Open text", command=openFile)
subMenu1.add_command(label="Save as", command=saveFile)
subMenu1.add_separator()
subMenu1.add_command(label="open simulator", command=openSim)
subMenu1.add_command(label="exit", command=exit)

subMenu2 = Menu(menu)
menu.add_cascade(label="actions", menu=subMenu2)
subMenu2.add_command(label="print containers", command=printCont)
subMenu2.add_command(label="add container", command=addCont)
subMenu2.add_command(label="add task", command=addTaskToContainer)
subMenu2.add_command(label="remove container", command=removeCont)
subMenu2.add_command(label="move robotic hand", command=moveRoboticArm)
subMenu2.add_command(label="set home position", command=setHomePosition)
subMenu2.add_command(label="start winery", command=startWinery)

subMenu3=Menu(menu)
menu.add_cascade(label="containers", menu=subMenu3)


subMenu4=Menu(menu)
menu.add_cascade(label="help", menu=subMenu4)
subMenu4.add_command(label="About", command=mesBox)


e1 = Entry(root)


root.mainloop()
