from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time

# master = Tk()
# choices = [("Apple", "a"), ("Orange", "o"), ("Pear", "p")]
# defaultChoice = "a"
# userchoice = StringVar()
# userchoice.set(defaultChoice)
# def cancelAction(): userchoice.set("");master.quit()
# Label(master, text="Choose a fruit:").pack()
# for text, key in choices:
#   Radiobutton(master, text=text, variable=userchoice, value=key).pack(anchor=W)
# Button(master, text="OK", command=master.quit).pack(side=LEFT, ipadx=10)
# Button(master, text="Cancel", command=cancelAction).pack(side=RIGHT, ipadx=10)
# mainloop()
# if 2>0:#userchoice.get() <>"":
#   print (userchoice.get()) # "a", or "o", or "p"
# else:
#   print ("Choice canceled.")


#
# master = Tk()
# choices = ["Apple", "Orange", "Pear"]
# canceled = BooleanVar()
# def cancelAction(): canceled.set(True); master.quit()
# Label(master, text="Choose a fruit:").pack()
# listbox = Listbox(master, selectmode=EXTENDED) # Multiple options can be chosen
# for text in choices:
#   listbox.insert(END, text)
# listbox.pack()
# Button(master, text="OK", command=master.quit).pack(side=LEFT, ipadx=10)
# Button(master, text="Cancel", command=cancelAction).pack(side=RIGHT, ipadx=10)
# mainloop()
# if not canceled.get():
#   print (listbox.curselection()) # A tuple of choice indices starting with 0
#   # The above is a tuple even if selectmode=SINGLE
#   if "0" in listbox.curselection(): print ("Apple chosen.")
#   if "1" in listbox.curselection(): print ("Orange chosen.")
#   if "2" in listbox.curselection(): print ("Pear chosen.")
# else:
#   print ("Choice canceled.")


# root = Tk()
# checkbuttonState = IntVar()
# Checkbutton(root, text="Recursive", variable=checkbuttonState).pack()
# mainloop()
# print (checkbuttonState.get()) # 1 = checked; 0 = unchecked


# root = Tk()
# Label(text="Enter your first name:").pack()
# entryContent = StringVar()
# Entry(root, textvariable=entryContent).pack()
# mainloop()
# print (entryContent.get())


# root = Tk()
# Label(text="Bus").pack()
# frame = LabelFrame(root, text="Fruits") # text is optional
# frame.pack()
# Label(frame, text="Apple").pack()
# Label(frame, text="Orange").pack()
# mainloop()


# root = Tk()
# options = ["Apple", "Orange", "Pear"]
# selectedOption = StringVar()
# # selectedOption.set("Apple") # Default
# OptionMenu(root, selectedOption, *options).pack()
# mainloop()
# print (selectedOption.get()) # The text in the options list



