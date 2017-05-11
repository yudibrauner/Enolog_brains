# https://www.youtube.com/watch?v=Ko4EPJ8DDjg#t=73.308091
from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time


# functions:


def openFile():
    adress = askopenfilename()

def saveFile():
    adress = asksaveasfilename()


def mesBox():
    tkinter.messagebox.showinfo("About Us:", "Yehuda Brauner\nElyashiv Miller")








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
subMenu1.add_command(label="XXXXXXXX")
subMenu1.add_command(label="exit", command=exit)

subMenu2 = Menu(menu)
menu.add_cascade(label="actions", menu=subMenu2)
subMenu2.add_command(label="add container", command=addContainer)


subMenu3=Menu(menu)
menu.add_cascade(label="containers", menu=subMenu3)
# here we need to add a button for every container


subMenu4=Menu(menu)
menu.add_cascade(label="help", menu=subMenu4)
subMenu4.add_command(label="About", command=mesBox)



button1 = Button(topFrame, text='Open simulation', fg='blue')
button2 = Button(topFrame, text='Close simulation', fg='blue')
# button3 = Button(topFrame, text='Button 3', fg='blue')
# button4 = Button(bottomFrame, text='Button 4', fg='red')

# button1.pack()
# button2.pack()
# button3.pack(side=LEFT)
# button4.pack()

root.mainloop()







