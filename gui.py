# https://www.youtube.com/watch?v=Ko4EPJ8DDjg#t=73.308091

from tkinter import *

root = Tk()
topFrame = Frame()
bottomFrame = Frame()
topFrame.pack(side=TOP)
bottomFrame.pack(side=BOTTOM)

button1 = Button(topFrame, text='Button 1', fg='blue')
button2 = Button(topFrame, text='Button 2', fg='green')
button3 = Button(topFrame, text='Button 3', fg='purple')
button4 = Button(bottomFrame, text='Button 4', fg='red')

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack()

root.mainloop()

