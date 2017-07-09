# This class represents a container of wine
import datetime
import random
from data_generator import *
from tkinter import *
from tkinter.filedialog import *
# from new_main_II import *
import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use("TKAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import pylab
import os
import time
import threading
import multiprocessing
from logger import *
import tkinter.scrolledtext as ScrolledText
from tkinter.font import Font
from decider import *


NO_DETAILS = "N/A"
EMPTY_IMAGE = "images/container.png"
FULL_IMAGE = "images/containerAct.png"
EMPTY_CONT_IMAGE = "images/emptyCont.png"
FULL_CONT_IMAGE = "images/fullCont.png"
SLOW_LIST = ('data\Tannins_slow.txt', 'data\Color_slow.txt', 'data\Density_slow.txt', 'data\Temperature_slow.txt')
NORMAL_LIST = ('data\Tannins_normal.txt', 'data\Color_normal.txt', 'data\Density_normal.txt', 'data\Temperature_normal.txt')
FAST_LIST = ('data\Tannins_fast.txt', 'data\Color_fast.txt', 'data\Density_fast.txt', 'data\Temperature_fast.txt')
PROGRAMS = {'No Program': 'No Program',
            'Slow': SLOW_LIST,
            'Normal': NORMAL_LIST,
            'Fast': FAST_LIST}
SENSORS = ('Tannins', 'Color', 'Density', 'Temperature')
# plt.style.use('fivethirtyeight')
BACKGROUND = '#37474f'
CONT_NAME_BG = '#78909C'


class Container:
    def __init__(self, _id, _place, root, interval):
        self.id = _id            # number of container in winery
        self.frame = root
        self.specFrame = LabelFrame(self.frame, bg=BACKGROUND, width=139, height=116)
        self.startDateTime = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        self.tasks = list()
        self.newImage = PhotoImage(file=EMPTY_CONT_IMAGE)
        self.interval = interval
        self.animationInterval = interval * 1000
        self.temperature = StringVar()
        self.tannins = StringVar()
        self.color = StringVar()
        self.density = StringVar()
        self.name = StringVar()
        self.program = StringVar()
        self.densityLabel = None
        self.buttonFunction = self.addCont
        self.isFull = False
        self.place = _place
        self.image = None
        self.photo = None
        self.idLabel = None
        self.densityValLabel = None
        self.tanninsValLabel = None
        self.colorValLabel = None
        self.temperatureValLabel = None
        self.densityValLabel_in_details = None
        self.tanninsValLabel_in_details = None
        self.colorValLabel_in_details = None
        self.temperatureValLabel_in_details = None
        self.nameLabel = None
        self.graph_plot = Figure(figsize=(8, 6), dpi=100)
        self.sub_plot_221 = self.graph_plot.add_subplot(221)
        self.sub_plot_222 = self.graph_plot.add_subplot(222)
        self.sub_plot_223 = self.graph_plot.add_subplot(223)
        self.sub_plot_224 = self.graph_plot.add_subplot(224)
        self.sub_plot_221.title.set_text('Tannins')
        self.sub_plot_222.set_title('Color')
        self.sub_plot_223.set_title('Density')
        self.sub_plot_224.set_title('Temperature')
        self.data_221 = None
        self.data_222 = None
        self.data_223 = None
        self.data_224 = None
        self.ani221 = None
        self.ani222 = None
        self.ani223 = None
        self.ani224 = None
        self.data_221_new = None
        self.initParams()
        self.dynamic_data = None
        self.generator = None
        self.frame.grid(row=0, column=0, columnspan=2)
        self.logger = None
        self.logger_name = None
        self.generator_thread = None
        self.decider = None
        self.text_handler = None
        self.st = None
        self.rootCont = None

    def setImage(self):
        self.photo = PhotoImage(file=self.image)
        # contButton = Button(self.frame, height=44, width=52, image=self.photo, relief=FLAT, background=BACKGROUND, command=self.buttonFunction)
        # contButton.place(x=self.place[0], y=self.place[1])
        newContButton = Button(self.specFrame, height=106, width=129, image=self.photo, relief=FLAT, background=BACKGROUND, command=self.buttonFunction)
        self.specFrame.place(x=self.place[0], y=self.place[1])
        newContButton.place(x=0, y=0)

    def initLabels(self):
        nameFont = Font(family="Times New Roman", size=13, weight='bold')
        labelFont = Font(family="Times New Roman", size=8)

        self.idLabel = Label(self.specFrame, text=str(self.id) + ': ', background=BACKGROUND)
        self.idLabel.place(x=self.place[0] + 10, y=self.place[1] - 30)

        self.nameLabel = Label(self.specFrame, textvariable=str(self.name), font=nameFont, background=CONT_NAME_BG)
        self.nameLabel.place(x=70 - 10*len(self.name.get())/2, y=83)

        self.densityValLabel = Label(self.specFrame, textvariable=str(self.density), background=BACKGROUND)
        self.densityValLabel.place(x=70, y=83)

        self.tanninsValLabel = Label(self.specFrame, textvariable=str(self.tannins), background=BACKGROUND)
        self.tanninsValLabel.place(x=self.place[0] + 35, y=self.place[1] + 90)

        self.colorValLabel = Label(self.specFrame, textvariable=str(self.color), background=BACKGROUND)
        self.colorValLabel.place(x=self.place[0] + 35, y=self.place[1] + 110)

        self.temperatureValLabel = Label(self.specFrame, textvariable=str(self.temperature), background=BACKGROUND)
        self.temperatureValLabel.place(x=self.place[0] + 35, y=self.place[1] + 130)

    def initParams(self):
        self.temperature.set(NO_DETAILS)
        self.tannins.set(NO_DETAILS)
        self.color.set(NO_DETAILS)
        self.density.set(NO_DETAILS)
        self.name.set(NO_DETAILS)
        self.program.set(PROGRAMS.get('No Program'))
        self.image = EMPTY_CONT_IMAGE
        self.setImage()

    def fillContainer(self):
        self.updateParams()
        self.isFull = True
        self.image = FULL_IMAGE
        self.image = FULL_CONT_IMAGE
        self.buttonFunction = self.showDetails
        self.setImage()
        self.initLabels()

    def updateParams(self):
        self.temperature.set(random.randrange(15, 40))
        self.tannins.set(random.randrange(4, 81))
        self.color.set(random.randrange(1, 6))
        self.density.set(random.randrange(970, 1300))

    def addDetails(self, rootCont, nameEntry):
        name = nameEntry.get()
        program = self.program.get()
        if name and program != 'No Program':
            self.name.set(name)
            print('-> container added')
            # Configure logger
            self.logger_name = str(self.name.get()) + '_' + str(self.id)
            #logging.basicConfig(filename='logs/' + self.logger_name + '.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

            # Add the handler to logger
            self.logger = logging.getLogger(self.logger_name)
            logging.basicConfig(filename='logs/' + self.logger_name + '.log',
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger.info('-> container added')

            self.fillContainer()
            self.buttonFunction = self.showDetails
            self.data_221 = PROGRAMS[program][0]
            self.data_222 = PROGRAMS[program][1]
            self.data_223 = PROGRAMS[program][2]
            self.data_224 = PROGRAMS[program][3]
            self.dynamic_data = 'data/dynamic_data/' + str(self.id) + '_' + str(self.name.get())
            self.generator = DataGenerator(self, self.dynamic_data, PROGRAMS[self.program.get()], self.interval, self.logger)
            self.generator_thread = threading.Thread(target=self.generator.start_generating, daemon=True)
            self.generator_thread.start()
            print('-> container added')
            rootCont.destroy()

    def addCont(self):
        self.rootCont = Toplevel()
        self.rootCont.wm_title("Adding container " + str(self.id))
        contFrame = Frame(self.rootCont, width=300, height=500)
        contFrame.pack()

        nameLabel = Label(contFrame, text='Name (wine type): ')
        nameEntry = Entry(contFrame)
        nameLabel.place(x=40, y=100)
        nameEntry.place(x=40, y=130)

        programLabel = Label(contFrame, text='Fermentation Program: ')
        programEntry = OptionMenu(contFrame, self.program, *PROGRAMS.keys())
        programLabel.place(x=40, y=160)
        programEntry.place(x=40, y=190)

        insertButton = Button(contFrame, text='Insert details', command=lambda: self.addDetails(self.rootCont, nameEntry))
        insertButton.place(x=40, y=350)

    def clearAllVariables(self, rootCont):
        new_container = Container(self.id, self.place, self.frame, self.interval)
        # TODO: add this new container to allContainers from main and remove previous container from there.
        # swapNewForOldContainer(self.id, new_container)
        self.id = NO_DETAILS
        self.temperature.set(None)
        self.tannins.set(None)
        self.color.set(None)
        self.density.set(None)
        self.name.set(None)
        self.idLabel.place_forget()
        self.nameLabel.place_forget()
        self.temperatureValLabel.place_forget()
        self.tanninsValLabel.place_forget()
        self.colorValLabel.place_forget()
        self.densityValLabel.place_forget()
        # os.remove(self.log['file_path'])
        self.logger = None
        self.generator.stay_alive = False
        rootCont.destroy()

    def endProcess(self, rootCont):
        msgBox = messagebox.askyesno('End Process ' + str(self.id) + ': ' + str(self.name.get()), 'Are you sure you want to end this process?', master=rootCont)
        if msgBox:
            self.logger.info('-> End of Process')
            self.logger.handlers = []
            self.generator.updateLogger(self.logger)
            self.clearAllVariables(rootCont)
            print('-> process ended')
            self.rootCont = Toplevel()
            self.rootCont.wm_title("Rate The Wine")
            frame = Frame(self.rootCont, width=200, height=150)
            frame.pack()
            scoreLabel = Label(frame, text='Score [0-100]: ')
            scoreEntry = Entry(frame)
            scoreLabel.place(x=40, y=40)
            scoreEntry.place(x=40, y=70)

            def addToDataBase(rootCont):
                # TODO: put data in DB (scoreEntry + self.generator.file)
                if int(scoreEntry.get()) not in list(range(0, 101)):
                    print('Invalid Score -> Try Again')
                    print(str(scoreEntry.get()))
                else:
                    print('Adding score and process to DB: ' + str(scoreEntry.get()) + ' + ' + str(self.generator.file))
                    rootCont.destroy()

            saveButton = Button(frame, text='Save', command=lambda: addToDataBase(self.rootCont))
            saveButton.place(x=100, y=100)

            dontSaveButton = Button(frame, text='Don\'t Save', command=self.rootCont.destroy)
            dontSaveButton.place(x=20, y=100)


    def showDetails(self):
        self.rootCont = Toplevel()
        self.rootCont.wm_title("Container " + str(self.id) + ': ' + str(self.name.get()))
        contFrameRight = LabelFrame(self.rootCont, width=400, height=500)
        contFrameRight.pack(side="right")
        # contFrameLeft = LabelFrame(self.rootCont, width=200, height=500)
        # contFrameLeft.pack(side="left")
        contFramebottom = LabelFrame(self.rootCont, width=1000, height=250)
        contFramebottom.pack(side="bottom")

        currentDetailsFrame = LabelFrame(self.rootCont, width=80, height=120, text="details")
        currentDetailsFrame.place(x=20, y=20)
        # logFrame = LabelFrame(contFramebottom, width=200, height=250, text="log")
        # logFrame.place()

        # Add text widget to display logging info
        self.st = ScrolledText.ScrolledText(contFramebottom)  # , state='disabled')
        self.st.configure(font='TkFixedFont')
        self.st.grid(column=0, row=1, sticky='w', columnspan=10)

        # Create textLogger
        self.text_handler = TextHandler(self.st)
        self.logger.addHandler(self.text_handler)

        densityLabel = Label(currentDetailsFrame, text='Dns: ')
        densityLabel.place(x=5, y=10)
        self.densityValLabel_in_details = Label(currentDetailsFrame, textvariable=str(self.density))
        self.densityValLabel_in_details.place(x=35, y=10)

        tanninsValLabel = Label(currentDetailsFrame, text='Tnn: ')
        tanninsValLabel.place(x=5, y=30)
        tanninsValLabel = Label(currentDetailsFrame, textvariable=str(self.tannins))
        tanninsValLabel.place(x=35, y=30)

        colorValLabel = Label(currentDetailsFrame, text='Clr: ')
        colorValLabel.place(x=5, y=50)
        colorValLabel = Label(currentDetailsFrame, textvariable=str(self.color))
        colorValLabel.place(x=35, y=50)

        temperatureValLabel = Label(currentDetailsFrame, text='Tmp: ')
        temperatureValLabel.place(x=5, y=70)
        temperatureValLabel = Label(currentDetailsFrame, textvariable=str(self.temperature))
        temperatureValLabel.place(x=35, y=70)

        canvas = FigureCanvasTkAgg(self.graph_plot, contFrameRight)
        canvas.get_tk_widget().pack(side=tk.RIGHT, expand=True)
        self.ani221 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_221, self.data_221, 1), interval=self.animationInterval)
        self.ani222 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_222, self.data_222, 2), interval=self.animationInterval)
        self.ani223 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_223, self.data_223, 3), interval=self.animationInterval)
        self.ani224 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_224, self.data_224, 4), interval=self.animationInterval)

        endProcessButton = Button(self.rootCont, text='End Process', command=lambda: self.endProcess(self.rootCont))
        endProcessButton.place(x=60, y=600)

        # rootCont.mainloop()

        def onExit():
            self.logger.removeHandler(self.text_handler)
            self.rootCont.destroy()
        self.rootCont.protocol('WM_DELETE_WINDOW', onExit)  # root is your root window

        self.rootCont.bind('<Escape>', lambda e: onExit())       # you can press escape to exit this frame

    def animate(self, i, sub_plot, data, sensor_type_index):         # sensor_type_index=index for parsing from generated data
        pullData = open(data, 'r').read()
        dataList = pullData.split('\n')
        xList = []
        yList = []
        for eachLine in dataList:
            if len(eachLine) > 1:
                x, y = eachLine.split(' ')
                xList.append(float(x))
                yList.append(float(y))

        pullDynamicData = open(self.dynamic_data, 'r').read()
        dynamicdataList = pullDynamicData.split('\n')
        xdynList = []
        ydynList = []
        for eachLine in dynamicdataList:
            if len(eachLine) > 1:
                parts = eachLine.split(' ')
                xdynList.append(float(parts[0]))
                ydynList.append(float(parts[sensor_type_index]))
        sub_plot.clear()
        sub_plot.set_title(SENSORS[sensor_type_index-1])
        self.graph_plot.subplots_adjust(hspace=.5)
        sub_plot.plot(xList, yList, '#00A3E0', label='Expected')
        sub_plot.plot(xdynList, ydynList, '#183A54', label='Observed')
        sub_plot.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)

    # SETTERS:
    def setInterval(self, interval):
        self.interval = interval

    def setTannin(self, tannin):
        self.tannins.set(tannin)

    def setColor(self, color):
        self.color.set(color)

    def setDensity(self, density):
        self.density.set(density)

    def setTemperature(self, temperature):
        self.temperature.set(temperature)

    def setNumber(self, num):
        self.id = num

    def setName(self, _name):
        self.name = _name

# OTHER FUNCTIONS:

    def cool(self):
        self.temperature -= 5

    def regulate(self): #TODO : ask Shivi how the regulator affects the color, density...
        print("there's nothing yet")
    #
    # def addTask(self, taskName):
    #     if taskName in TASK_NAMES:
    #         task = Task(taskName)
    #         self.tasks.append(task)
    #     else:
    #         print('-> ERROR: not a task')
    #
    # def tasksToString(self):
    #     lst = ''
    #     for t in self.tasks:
    #         lst += str(t.task) + ','
    #     return lst

    def printContainer(self):
        print('Name: ' + str(self.name.get()))
        print('Winery Container Number: ' + str(self.id))
        print('Creation date&time: ' + str(self.startDateTime))
        print('Tasks: ' + self.tasksToString())
        print('Temperature: ' + str(self.temperature.get()) + '°C')
