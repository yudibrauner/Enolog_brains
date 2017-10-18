import csv
import sqlite3
from container import *

#INIT:

allContainers = []
matrixDB = {'general': [], 'containers': []}
num_of_containers = 10
NO_NOTES = 'There are no notes'
BACKGROUND = '#37474f'
FONTITLE_COLOR = '#FFD966'

ANIMATION_INTERVAL = 1
names_of_tables = []

# GUI

root = Tk()
root.wm_title("Smart winery app")

# FRAMES:

mainFrame = Frame(root, width=1000, height=600, bg=BACKGROUND)
mainFrame.pack()

note = StringVar(value=NO_NOTES)

def settings():
    #  TODO: fix up this popup
    rootCont = Tk()
    rootCont.wm_title("Settings")
    contFrame = Frame(rootCont, width=300, height=500)
    contFrame.pack()
    numOfContainersLabel = Label(contFrame, text='Set number of containers: ')
    numOfContainersEntry = Entry(contFrame, text=str(num_of_containers))
    sensorsIntervalLabel = Label(contFrame, text='Set Sensors Interval (sec): ')
    sensorsIntervalEntry = Entry(contFrame, text=str(ANIMATION_INTERVAL))
    numOfContainersLabel.place(x=40, y=100)
    numOfContainersEntry.place(x=40, y=130)
    sensorsIntervalLabel.place(x=40, y=160)
    sensorsIntervalEntry.place(x=40, y=190)

    def addDetails():
        numOfContainers = numOfContainersEntry.get()
        ANIMATION_INTERVAL = sensorsIntervalEntry.get()
        for container in allContainers:
            container.setInterval(ANIMATION_INTERVAL)
            if container.isFull:
                container.generator.setInterval(ANIMATION_INTERVAL)
        print('->  Number of containers set to: ' + numOfContainers)
        print('->  Sensors Interval set to: ' + ANIMATION_INTERVAL)
        rootCont.destroy()

    cancelButton = Button(contFrame, text='Cancel', command=rootCont.destroy)
    cancelButton.place(x=40, y=300)
    insertButton = Button(contFrame, text='OK', command=addDetails)
    insertButton.place(x=150, y=300)

def swapNewForOldContainer(old_id, new_container):
    for container in allContainers:
        if container.id == old_id:
            allContainers.remove(container)
    allContainers.append(new_container)

# MAIN:
titleFont = Font(family="Times New Roman", size=30)
noteFont = Font(family="Times New Roman", size=15)
title = Label(mainFrame, text='WINERY DASHBOARD', background=BACKGROUND, font=titleFont, fg=FONTITLE_COLOR)
title.place(x=300, y=10)
noteLabel = Label(mainFrame, text='note:', background=BACKGROUND, font=noteFont, fg='white')
noteLabel.place(x=400, y=550)
notesLabel = Label(mainFrame, textvariable=str(note), background=BACKGROUND, font=noteFont, fg='white')
notesLabel.place(x=450, y=550)

def saveSQL():
    DBfile = sqlite3.connect('DB/smart winery.db')
    c = DBfile.cursor()
    names_of_tables = []
    general_name = 'generalFermentations'# + str(datetime.datetime.now().strftime("%d%m%y%H%M%S"))
    names_of_tables.append(general_name)
    c.execute('drop table if exists ' + general_name)
    c.execute('CREATE TABLE ' + general_name + '''
                (Container_id, Fermentation, Wine_name, Mistakes, Score, Start, End,
                C_Quality, C_Strength, S_Centralization, S_Originality, S_Quality,
                T_Centralization, T_Originality, T_Quality, T_Residual,
                General_ranking, Note, Vintner)''')
    for container in matrixDB['general']:
        print(container)
        c.execute("INSERT INTO " + general_name + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (container['Container id'], container['Fermentation'], container['Wine name'], container['Mistakes'], container['Score'], container['Start'], container['End'],
                   container['C: Quality'], container['C: Strength'], container['S: Centralization'], container['S: Originality'], container['S: Quality'],
                    container['T: Centralization'], container['T: Originality'], container['T: Quality'], container['T: Residual'],
                    container['General ranking'], container['Note'], container['Vintner']))

    for container in matrixDB['containers']:
        general_name = 'container_' + container['name'] + '_' + str(container['id'])
        names_of_tables.append(general_name)
        c.execute('drop table if exists ' + general_name)
        c.execute('CREATE TABLE ' + general_name + '''
                        (hours_from_start, expected_tannins, expected_color, expected_temperature, expected_density,
                        expected_cool_acts, expected_pump_acts, top_tannins_sensor, middle_tannins_sensor, bottom_tannins sensor,
                        top_color_sensor, middle_color_sensor, bottom_color_sensor, top_temperature_sensor,
                        middle_temperature_sensor, bottom_temperature_sensor, top_density_sensor, middle_density_sensor,
                        bottom_density_sensor, cool_acts, pump_acts, date, time)''')
        for line in container['log']:
            c.execute("INSERT INTO " + general_name + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (line['hours from start'], line['expected tannins'], line['expected color'],
                       line['expected temperature'], line['expected density'], line['expected cool acts'],
                       line['expected pump acts'], line['top tannins sensor'], line['middle tannins sensor'],
                       line['bottom tannins sensor'], line['top color sensor'], line['middle color sensor'],
                       line['bottom color sensor'], line['top temperature sensor'], line['middle temperature sensor'],
                       line['bottom temperature sensor'], line['top density sensor'], line['middle density sensor'],
                       line['bottom density sensor'], line['cool acts'], line['pump acts'], line['date'], line['time']))
    DBfile.commit()
    DBfile.close()

def saveCSV():
    general_name = 'general fermentations ' + str(datetime.datetime.now().strftime("%d %m %y %H %M %S"))
    adress = 'DB/' + general_name + '.csv'
    with open(adress, 'w') as csvfile:
        fieldnames = ['Container id', 'Fermentation', 'Wine name', 'Mistakes', 'Score', 'Start', 'End',
                      'C: Quality', 'C: Strength', 'S: Centralization', 'S: Originality', 'S: Quality', 'T: Centralization',
                      'T: Originality', 'T: Quality', 'T: Residual', 'General ranking', 'Note', 'Vintner']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matrixDB['general'])
    for container in matrixDB['containers']:
        general_name = 'container ' + container['name'] + ' ' + str(container['id'])
        adress = 'DB/' + general_name + '.csv'
        with open(adress, 'w') as csvfile:
            fieldnames = ['hours from start', 'expected tannins', 'expected color', 'expected temperature',
                          'expected density', 'expected cool acts', 'expected pump acts', 'top tannins sensor',
                          'middle tannins sensor', 'bottom tannins sensor', 'top color sensor', 'middle color sensor',
                          'bottom color sensor', 'top temperature sensor', 'middle temperature sensor', 'bottom temperature sensor',
                          'top density sensor', 'middle density sensor', 'bottom density sensor', 'cool acts', 'pump acts', 'date', 'time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(container['log'])

def about():
    x=5

def printTABLE():
    rootSQL = Tk()
    rootSQL.wm_title("Ask SQLite")
    ansFrame = Frame(rootSQL, width=300, height=500)
    ansFrame.pack()
    DBfile = sqlite3.connect('DB/smart winery.db')
    c = DBfile.cursor()
    res = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    names_of_tables = []
    for name in res:
        names_of_tables.append(name[0])
    DBfile.commit()
    DBfile.close()
    st = ScrolledText.ScrolledText(ansFrame, wrap=tk.WORD, width=115, height=20)
    st.configure(font='TkFixedFont')
    st.grid(column=0, row=1, sticky='w', columnspan=10)
    for table in names_of_tables:
        DBfile = sqlite3.connect('DB/smart winery.db')
        c = DBfile.cursor()
        str = 'SELECT * FROM ' + table
        c.execute(str)
        answer = c.fetchall()
        st.insert(INSERT, table + ":\n\n")
        st.insert(INSERT, answer)
        st.insert(INSERT, "\n\n________________________________________________________________\n\n\n")
        DBfile.commit()
        DBfile.close()

#creats line to enter questions to the SQLite
def askTABLE():
    rootSQL = Tk()
    rootSQL.wm_title("Ask SQLite")
    DBfile = sqlite3.connect('DB/smart winery.db')
    c = DBfile.cursor()
    res = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    names_of_tables = []
    for name in res:
        names_of_tables.append(name[0])
    DBfile.commit()
    DBfile.close()
    askFrame = Frame(rootSQL, width=600, height=70)
    askFrame.pack(side=TOP)
    ansFrame = Frame(rootSQL, width=300, height=500)
    ansFrame.pack(side=BOTTOM)
    nameFont = Font(family="Times New Roman", size=13, weight='bold')
    Label(ansFrame, text="Current tables are: " + str(names_of_tables), font=nameFont).grid(column=0, row=0, sticky='w', columnspan=10)
    st2 = ScrolledText.ScrolledText(ansFrame, wrap=tk.WORD, width=115, height=20)
    st2.configure(font='TkFixedFont')
    st2.grid(column=0, row=1, sticky='w', columnspan=10)

    def enterAsk():
        str = askEntry.get()
        DBfile = sqlite3.connect('DB/smart winery.db')
        c = DBfile.cursor()
        c.execute(str)
        answer = c.fetchall()
        st2.insert(INSERT, str + ":\n\n")
        st2.insert(INSERT, answer)
        st2.insert(INSERT, "\n\n________________________________________________________________\n\n\n")
        DBfile.commit()
        DBfile.close()

    Label(askFrame, text='Ask:').place(x=50, y=20)
    askEntry = Entry(askFrame, width=150)
    askEntry.insert(INSERT,'SELECT * FROM generalFermentations')
    askEntry.place(x=100, y=20)
    Button(askFrame, text='Enter', command=enterAsk).place(x=5,y=20)

# creating all the containers
for i in range(0, 5):
    for j in range(0, 2):
        id = (i+1)*(j+1)
        place = (170 * i + 100, 250*j + 130)
        allContainers.append(Container(id, place, mainFrame, ANIMATION_INTERVAL, matrixDB, note))

menu=Menu(root)
root.config(menu=menu)

subMenu1=Menu(menu)
menu.add_cascade(label="file", menu=subMenu1)
subMenu1.add_command(label="Save as CSV", command=saveCSV)
subMenu1.add_command(label="Save as SQL", command=saveSQL)
subMenu1.add_separator()
subMenu1.add_command(label="Exit", command=exit)

subMenu2=Menu(menu)
menu.add_cascade(label="SQLite", menu=subMenu2)
subMenu2.add_command(label="Print DB", command=printTABLE)
subMenu2.add_command(label="Ask with SQLite", command=askTABLE)

subMenu3=Menu(menu)
menu.add_cascade(label="help", menu=subMenu3)
subMenu3.add_command(label="About", command=about)

root.mainloop()