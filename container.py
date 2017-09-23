# This class represents a container of wine

import datetime
import random
import tkinter as tk
import matplotlib
matplotlib.use("TKAgg")
import pylab
import os
import time
import threading
import multiprocessing
import tkinter.messagebox
import helpFunctions

import matplotlib.animation as animation
import tkinter.scrolledtext as ScrolledText
import matplotlib.pyplot as plt

from data_generator import *
from sensors import *
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from logger import *
from tkinter.font import Font
from decider import *


# vars:

NO_DETAILS = "N/A"
# images:
EMPTY_IMAGE = "images/container.png"
FULL_IMAGE = "images/containerAct.png"
EMPTY_CONT_IMAGE = "images/emptyCont.png"
FULL_CONT_IMAGE = "images/fullCont.png"
FINISH_CONT_IMAGE = "images/finishCont.png"
END_PROCESS_IMAGE = "images/EndProcess.png"
#programs:
SLOW_LIST = ('data\Tannins_slow.txt', 'data\Color_slow.txt', 'data\Density_slow.txt', 'data\Temperature_slow.txt')
NORMAL_LIST = ('data\Tannins_normal.txt', 'data\Color_normal.txt', 'data\Density_normal.txt', 'data\Temperature_normal.txt')
FAST_LIST = ('data\Tannins_fast.txt', 'data\Color_fast.txt', 'data\Density_fast.txt', 'data\Temperature_fast.txt')
PROGRAMS = {'Slow': SLOW_LIST, 'Normal': NORMAL_LIST, 'Fast': FAST_LIST, 'Create a new ferm.': 'new'}
# rates:
COLOR_QUALITY = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
COLOR_POWER = {'2': 2, '4': 4, '6': 6, '8': 8, '10': 10}
SMELL_OZ = {'2': 2, '4': 4, '6': 6, '7': 7, '8': 8}
SMELL_SOURCE = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
SMELL_QUALITY = {'8': 8, '10': 10, '12': 12, '14': 14, '16': 16}
TASTE_OZ = {'2': 2, '4': 4, '6': 6, '7': 7, '8': 8}
TASTE_SOURCE = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
TASTE_QUALITY = {'10': 10, '13': 13, '16': 16, '19': 19, '22': 22}
TASTE_SHIUR = {'4': 4, '5': 5, '6': 6, '7': 7, '8': 8}
GENERAL_RATE = {'7': 7, '8': 8, '9': 9, '10': 10, '11': 11}
# arrays:
SENSORS = ('Tannins', 'Color', 'Density', 'Temperature')
# plt.style.use('fivethirtyeight')

# colors:
BACKGROUND = '#37474f'
CONT_NAME_BG = '#78909C'
ATTRS_BG = '#E0E0E0'
EXPECTEDLINECOLOR = '#00A3E0'
OBSERVEDLINECOLOR = '#183A54'

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
        self.initStringVars()
        self.buttonFunction = self.addCont
        self.isFull = False
        self.place = _place
        self.initNones()
        self.initLabels()
        self.initGraphs()
        self.initParams()
        self.frame.grid(row=0, column=0, columnspan=2)

    def initStringVars(self):
        self.temperature = StringVar()
        self.tannins = StringVar()
        self.color = StringVar()
        self.density = StringVar()
        self.realTemperature = StringVar()
        self.realTannins = StringVar()
        self.realColor = StringVar()
        self.realDensity = StringVar()
        self.name = StringVar()
        self.program = StringVar()
        self.time = StringVar()
        self.date = StringVar()

    def initNones(self):
        self.image = None
        self.photo = None
        self.end_process_photo = None
        self.dynamic_data = None
        self.wine_data = None
        self.sensors_data = None
        self.generator = None
        self.logger = None
        self.logger_name = None
        self.generator_thread = None
        self.decider = None
        self.text_handler = None
        self.st = None
        self.rootCont = None

    def initLabels(self):
        self.densityLabel = None
        self.idLabel = None
        self.nameLabel = None
        self.densityValLabel = None
        self.tanninsValLabel = None
        self.colorValLabel = None
        self.temperatureValLabel = None
        self.densityValLabel_in_details = None
        self.tanninsValLabel_in_details = None
        self.colorValLabel_in_details = None
        self.temperatureValLabel_in_details = None

    def initGraphs(self):
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

    def setImage(self):
        self.photo = PhotoImage(file=self.image)
        # contButton = Button(self.frame, height=44, width=52, image=self.photo, relief=FLAT, background=BACKGROUND, command=self.buttonFunction)
        # contButton.place(x=self.place[0], y=self.place[1])
        newContButton = Button(self.specFrame, height=106, width=129, image=self.photo, relief=FLAT, background=BACKGROUND, command=self.buttonFunction)
        self.specFrame.place(x=self.place[0], y=self.place[1])
        newContButton.place(x=0, y=0)

    def startLabels(self):
        nameFont = Font(family="Times New Roman", size=13, weight='bold')
        labelFont = Font(family="Times New Roman", size=6)
        # self.idLabel = Label(self.specFrame, text=str(self.id) + ': ', background=BACKGROUND)
        # self.idLabel.place(x=self.place[0] + 10, y=self.place[1] - 30)
        self.nameLabel = Label(self.specFrame, textvariable=str(self.name), font=nameFont, background=CONT_NAME_BG)
        self.nameLabel.place(x=70 - 10*len(self.name.get())/2, y=83)
        self.temperatureValLabel = Label(self.specFrame, textvariable=str(self.realTemperature), background=ATTRS_BG, font=labelFont)
        self.temperatureValLabel.place(x=75, y=23)
        self.densityValLabel = Label(self.specFrame, textvariable=str(self.realDensity), background=ATTRS_BG, font=labelFont)
        self.densityValLabel.place(x=75, y=60)
        self.tanninsValLabel = Label(self.specFrame, textvariable=str(self.realTannins), background=ATTRS_BG, font=labelFont)
        self.tanninsValLabel.place(x=75, y=48)
        self.colorValLabel = Label(self.specFrame, textvariable=str(self.realColor), background=ATTRS_BG, font=labelFont)
        self.colorValLabel.place(x=75, y=35)
        self.end_process_photo = PhotoImage(file=END_PROCESS_IMAGE)

    def initParams(self):
        self.temperature.set(NO_DETAILS)
        self.tannins.set(NO_DETAILS)
        self.color.set(NO_DETAILS)
        self.density.set(NO_DETAILS)
        self.realTemperature.set(NO_DETAILS)
        self.realTannins.set(NO_DETAILS)
        self.realColor.set(NO_DETAILS)
        self.realDensity.set(NO_DETAILS)
        self.name.set(NO_DETAILS)
        self.time.set(NO_DETAILS)
        self.date.set(NO_DETAILS)
        self.program.set('No Program')
        self.image = EMPTY_CONT_IMAGE
        self.setImage()

    def fillContainer(self):
        #self.updateParams()
        self.isFull = True
        self.image = FULL_CONT_IMAGE
        self.buttonFunction = self.showDetails
        self.setImage()
        self.startLabels()

    def addDetails(self, rootCont, nameEntry):
        name = nameEntry.get()
        program = self.program.get()
        if program == 'Create a new ferm.':
            self.createNewProg()
        elif program == 'No Program':
            self.mesBox("Please choose a program.", "")
        elif name == "":
            self.mesBox("Please enter the wine's name.", "")
        else:
            self.name.set(name)
            # Configure logger
            self.logger_name = str(self.name.get()) + '_' + str(self.id)
            self.shortLogger_name = 'S_' + str(self.name.get()) + '_' + str(self.id)
            # Add the handler to logger
            self.logger = logging.getLogger(self.logger_name)
            logging.basicConfig(filename='logs/longLogs/' + self.logger_name + '.log',
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger.info('-> container added')

            # Add the handler to logger
            self.shortLogger = logging.getLogger(self.shortLogger_name)
            logging.basicConfig(filename='logs/shortLogs/' + self.shortLogger_name + '.log',
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')
            self.shortLogger.info('-> container addedgggg')

            self.fillContainer()
            self.buttonFunction = self.showDetails
            self.data_221 = PROGRAMS[program][0]
            self.data_222 = PROGRAMS[program][1]
            self.data_223 = PROGRAMS[program][2]
            self.data_224 = PROGRAMS[program][3]
            self.dynamic_data = 'data/dynamic_data/'
            self.wine_data = self.dynamic_data + 'generator/' + str(self.id) + '_' + str(self.name.get())
            self.sensors_data = self.dynamic_data + 'sensors/' + str(self.id) + '_' + str(self.name.get())
            self.generator = DataGenerator(self, self.wine_data, self.program.get(), PROGRAMS[self.program.get()], self.interval, self.logger)
            self.generator_thread = threading.Thread(target=self.generator.start_generating, daemon=True)
            self.generator_thread.start()
            self.sensors = Sensors(self, self.generator, self.sensors_data)
            rootCont.destroy()

    def createNewProg(self):
        self.mesBox('TODO IT', '')

    def addCont(self):
        self.rootCont = Toplevel()
        self.rootCont.wm_title("Adding container " + str(self.id))
        contFrame = Frame(self.rootCont, width=300, height=500)
        contFrame.pack()

        Label(contFrame, text='Name (wine type): ').place(x=40, y=100)
        nameEntry = Entry(contFrame)
        nameEntry.place(x=40, y=130)

        Label(contFrame, text='Fermentation Program: ').place(x=40, y=160)
        programEntry = OptionMenu(contFrame, self.program, *PROGRAMS.keys())
        programEntry.place(x=40, y=190)

        insertButton = Button(contFrame, text='Insert details', command=lambda: self.addDetails(self.rootCont, nameEntry))
        insertButton.place(x=40, y=350)

    def fermIsFinished(self):
        self.image = FINISH_CONT_IMAGE
        self.setImage()
        helpFunctions.sendMail(self.name.get() + "in container" + str(self.id) + "is finished")

    def clearAllVariables(self, rootCont):
        new_container = Container(self.id, self.place, self.frame, self.interval)
        # TODO: add this new container to allContainers from main and remove previous container from there.
        # swapNewForOldContainer(self.id, new_container)
        self.id = NO_DETAILS
        self.temperature.set(None)
        self.tannins.set(None)
        self.color.set(None)
        self.density.set(None)
        self.realTemperature.set(None)
        self.realTannins.set(None)
        self.realColor.set(None)
        self.realDensity.set(None)
        self.name.set(None)
        self.time.set(None)
        self.date.set(None)
        self.idLabel.place_forget()
        self.nameLabel.place_forget()
        self.temperatureValLabel.place_forget()
        self.tanninsValLabel.place_forget()
        self.colorValLabel.place_forget()
        self.densityValLabel.place_forget()
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

            self.rootCont = Toplevel()
            self.rootCont.wm_title("Rate The Wine")
            rateFrame = Frame(self.rootCont, width=600, height=500)
            rateFrame.pack()
            self.initRates()

            showFrame = LabelFrame(self.rootCont, width=500, height=80, text="מראה")
            showFrame.place(x=20, y=20)
            Label(showFrame, text='צבע איכות').place(x=10, y=10)
            CQEntry = OptionMenu(showFrame, self.rates[0], *COLOR_QUALITY.keys())
            CQEntry.place(x=100, y=10)
            Label(showFrame, text='צבע עוצמה').place(x=260, y=10)
            CPEntry = OptionMenu(showFrame, self.rates[1], *COLOR_POWER.keys())
            CPEntry.place(x=350, y=10)

            smellFrame = LabelFrame(self.rootCont, width=500, height=80, text="ריח")
            smellFrame.place(x=20, y=120)
            Label(smellFrame, text='ריכוזיות').place(x=10, y=10)
            SOEntry = OptionMenu(smellFrame, self.rates[2], *SMELL_OZ.keys())
            SOEntry.place(x=60, y=10)
            Label(smellFrame, text='מקוריות').place(x=150, y=10)
            SSEntry = OptionMenu(smellFrame, self.rates[3], *SMELL_SOURCE.keys())
            SSEntry.place(x=200, y=10)
            Label(smellFrame, text='איכות').place(x=290, y=10)
            SQEntry = OptionMenu(smellFrame, self.rates[4], *SMELL_QUALITY.keys())
            SQEntry.place(x=340, y=10)

            tasteFrame = LabelFrame(self.rootCont, width=500, height=80, text="טעם")
            tasteFrame.place(x=20, y=220)
            Label(tasteFrame, text='ריכוזיות').place(x=20, y=3)
            TOEntry = OptionMenu(tasteFrame, self.rates[5], *TASTE_OZ.keys())
            TOEntry.place(x=20, y=25)
            Label(tasteFrame, text='מקוריות').place(x=120, y=3)
            TSEntry = OptionMenu(tasteFrame, self.rates[6], *TASTE_SOURCE.keys())
            TSEntry.place(x=120, y=25)
            Label(tasteFrame, text='איכות').place(x=220, y=3)
            TQEntry = OptionMenu(tasteFrame, self.rates[7], *TASTE_QUALITY.keys())
            TQEntry.place(x=220, y=25)
            Label(tasteFrame, text='שיוריות').place(x=320, y=3)
            THEntry = OptionMenu(tasteFrame, self.rates[8], *TASTE_SHIUR.keys())
            THEntry.place(x=320, y=25)

            generalFrame = LabelFrame(self.rootCont, width=500, height=80, text="הערכה כללית")
            generalFrame.place(x=20, y=320)
            Label(generalFrame, text='דירוג כללי').place(x=20, y=20)
            GEntry = OptionMenu(generalFrame, self.rates[9], *GENERAL_RATE.keys())
            GEntry.place(x=100, y=20)
            Label(generalFrame, text='Note:').place(x=200, y=20)
            scoreEntry = Entry(generalFrame)
            scoreEntry.place(x=300, y=20)

            Label(rateFrame, text='Vinemaker:').place(x=20, y=420)
            nameEntry = Entry(rateFrame)
            nameEntry.place(x=80, y=420)

            def isFullFields(self):
                for rate in self.rates:
                    if rate.get() == 'No Rate':
                        return False
                return True

            def geneRate(self):
                for rate in self.rates:
                    if rate.get() == 'No Rate':
                        self.mesBox('no rate for ' + str(rate) + 'yet.', "TODO")

            def calculateScore(self):
                sum = 0
                for rate in self.rates:
                    sum += int(rate.get())
                return sum

            def addToDataBase(rootCont):
                # TODO: put data in DB (scoreEntry + self.generator.file)
                if nameEntry.get() and isFullFields(self):
                    calc = calculateScore(self)
                    print('Adding score and process to DB: ' + str(calc) + ' + ' + str(self.generator.file))
                    rootCont.destroy()
                else:
                    self.mesBox('You did not fill all the fields', 'Try Again')
            geneRateButton = Button(rateFrame, text='generate the rates', command=lambda: geneRate(self))
            geneRateButton.place(x=400, y=450)
            saveButton = Button(rateFrame, text='Save', command=lambda: addToDataBase(self.rootCont))
            saveButton.place(x=200, y=450)
            dontSaveButton = Button(rateFrame, text='Don\'t Save', command=self.rootCont.destroy)
            dontSaveButton.place(x=300, y=450)

    def initRates(self):
        self.rates = []
        for i in range (0, 10):
            self.rates.append(StringVar())
            self.rates[i].set('No Rate')

    def showDetails(self):
        self.rootCont = Toplevel()
        self.rootCont.wm_title("Container " + str(self.id) + ': ' + str(self.name.get()))
        # FRAMES:
        contFrameMain = Frame(self.rootCont, width=1250, height=700, bg='#37474f')
        contFrameMain.pack()
        titleFont = Font(family="Times New Roman", size=30)
        title = Label(contFrameMain, text=self.name.get(), background=BACKGROUND, font=titleFont, fg='#FFD966')
        title.place(x=550, y=10)
        contFrameGraphs = Frame(contFrameMain, width=650, height=535)
        contFrameGraphs.place(x=490, y=110)

        upContFrameLog = Frame(contFrameMain, width=385, height=300, background='#78909C')
        upContFrameLog.place(x=60, y=350)
        labelsFont = Font(family="Times New Roman", size=20)
        labelProcessLog = Label(upContFrameLog, text='Process Log', background='#78909C', font=labelsFont, fg='black')
        labelProcessLog.place(x=130, y=7)
        contFrameLog = Frame(upContFrameLog, width=385, height=250)
        contFrameLog.place(x=0, y=50)
        # Add text widget to display logging info
        self.st = ScrolledText.ScrolledText(contFrameLog)  # , state='disabled')
        self.st.configure(font='TkFixedFont')
        self.st.grid(column=0, row=1, sticky='w', columnspan=10)

        # Create textLogger
        self.text_handler = TextHandler(self.st)
        self.logger.addHandler(self.text_handler)

        upContFrameDetails = Frame(contFrameMain, width=270, height=220, background='#78909C')
        upContFrameDetails.place(x=175, y=110)
        # TODO: check why the time and date aren't good
        labelTime = Label(upContFrameDetails, textvariable=str(self.time), background='#78909C', font=labelsFont, fg='black')
        labelTime.place(x=10, y=5)
        labelDate = Label(upContFrameDetails, textvariable=str(self.date), background='#78909C', font=labelsFont, fg='black')
        labelDate.place(x=150, y=5)
        contFrameDetails = Frame(upContFrameDetails, width=270, height=180)
        contFrameDetails.place(x=0, y=40)

        densityLabel = Label(contFrameDetails, text='Density:')
        densityLabel.place(x=5, y=10)
        self.densityValLabel_in_details = Label(contFrameDetails, textvariable=str(self.realDensity))
        self.densityValLabel_in_details.place(x=80, y=10)

        tanninsValLabel = Label(contFrameDetails, text='Tannins:')
        tanninsValLabel.place(x=5, y=40)
        self.tanninsValLabel_in_details = Label(contFrameDetails, textvariable=str(self.realTannins))
        self.tanninsValLabel_in_details.place(x=80, y=40)

        colorValLabel = Label(contFrameDetails, text='Color:')
        colorValLabel.place(x=5, y=70)
        self.colorValLabel_in_details = Label(contFrameDetails, textvariable=str(self.realColor))
        self.colorValLabel_in_details.place(x=80, y=70)

        temperatureValLabel = Label(contFrameDetails, text='Temerature:')
        temperatureValLabel.place(x=5, y=100)
        self.temperatureValLabel_in_details = Label(contFrameDetails, textvariable=str(self.realTemperature))
        self.temperatureValLabel_in_details.place(x=80, y=100)

        endProcessButton = Button(contFrameMain, image=self.end_process_photo, command=lambda: self.endProcess(self.rootCont))
        endProcessButton.place(x=63, y=110)
        # TODO: check what the problem in the animations is.
        canvas = FigureCanvasTkAgg(self.graph_plot, contFrameGraphs)
        canvas.get_tk_widget().pack(side=tk.LEFT, expand=True)
        self.ani221 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_221, self.data_221, 1), interval=self.animationInterval)
        self.ani222 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_222, self.data_222, 2), interval=self.animationInterval)
        self.ani223 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_223, self.data_223, 3), interval=self.animationInterval)
        self.ani224 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_224, self.data_224, 4), interval=self.animationInterval)

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

        pullDynamicData = open(self.sensors_data, 'r').read()
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
        sub_plot.plot(xList, yList, EXPECTEDLINECOLOR, label='Expected')
        sub_plot.plot(xdynList, ydynList, OBSERVEDLINECOLOR, label='Observed')
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

    def setRealTannin(self, tannin):
        self.realTannins.set(tannin)

    def setRealColor(self, color):
        self.realColor.set(color)

    def setRealDensity(self, density):
        self.realDensity.set(density)

    def setRealTemperature(self, temperature):
        self.realTemperature.set(temperature)

    def setDateTime(self, dateTime):
        self.date = dateTime.split(' ')[0]
        self.time = dateTime.split(' ')[1]

    def setNumber(self, num):
        self.id = num

    def setName(self, _name):
        self.name = _name


# OTHER FUNCTIONS:

    def cool(self):
        self.temperature -= 5

    def regulate(self): #TODO : ask Shivi how the regulator affects the color, density...
        self.mesBox("there's nothing yet", 'todo')
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

    def mesBox(self, message, note):
        tkinter.messagebox.showinfo("Error", message + "\n" + note)

    def printContainer(self):
        print('Name: ' + str(self.name.get()))
        print('Winery Container Number: ' + str(self.id))
        print('Creation date&time: ' + str(self.startDateTime))
        print('Tasks: ' + self.tasksToString())
        print('Temperature: ' + str(self.temperature.get()) + '°C')
