from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time

container=[]

#function that takes adress of NMEA file, and add it to the DataBase and to the container.
def giveName(adress):
    currentList = []
    with open(adress, 'r') as file:
        data = file.readlines()
    DBfile = sqlite3.connect('temp.db')
    c = DBfile.cursor()
    c.execute('drop table if exists nmea' + str(len(container)))
    c.execute('CREATE TABLE nmea' + str(len(container)) + '''
                (name text, time time, length text, north text, wide text,
                east text, quality integer, nos text, hdop text, altitude real,
                hog text, speed real, date date)''')
    flag = 0#check if we entered all the lines to dictionary
    adresses = adress.split('/')
    nameDB = adresses[-1][:-4]
    #print(nameDB)
    for line in data:
        cur = line.split(',')
        currentDict = {}
        if (cur[0] == "$GPGGA" and cur[6] != "0"):
            currentDict['name'] = nameDB
            currentDict['time'] = format_time(cur[1])
            currentDict['length'] = cur[2]
            currentDict['north'] = cur[3]
            currentDict['wide'] = cur[4]
            currentDict['east'] = cur[5]
            currentDict['quality'] = int(cur[6])
            currentDict['nos'] = cur[7]
            currentDict['hdop'] = cur[8]
            currentDict['altitude'] = float(cur[9])
            currentDict['date'] = format_date("000000")
            currentDict['speed'] = knots_to_kph("0.1")
            currentDict['hog'] = cur[11]
            currentList.append(currentDict)
            flag=1
        else:
            if(cur[0] == "$GPRMC" and cur[2] == "A" and flag == 1):
                currentList[-1]['date'] = format_date(cur[9])
                currentList[-1]['speed'] = knots_to_kph(cur[7])
                flag=2
            if(flag==2):#if we finished the current dictionary wer'e adding it to the match table in the DB
                c.execute("INSERT INTO nmea" + str(len(container)) + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                    currentList[-1]['name'], currentList[-1]['time'], currentList[-1]['length'], currentList[-1]['north'], currentList[-1]['wide'], currentList[-1]['east'], currentList[-1]['quality'],
                    currentList[-1]['nos'], currentList[-1]['hdop'], currentList[-1]['altitude'], currentList[-1]['hog'], currentList[-1]['speed'], currentList[-1]['date']))
                flag=0
    container.append(currentList)
    #now, wer'e adding to DB a table with the important things of the nmea
    c.execute('select * from nmea'+str(len(container)-1))
    c.execute('''CREATE TABLE IF NOT EXISTS DB(name text, Date date, Length time,
        maxSpeed text, minSpeed text, maxHeight real, minHeight real, quality integer)''')
    c.execute('SELECT MIN(time) FROM nmea' + str(len(container) - 1))
    aTime = c.fetchall()[0][0]
    c.execute('SELECT MAX(time) FROM nmea' + str(len(container) - 1))
    bTime = c.fetchall()[0][0]
    c.execute('SELECT MIN(date) FROM nmea' + str(len(container) - 1))
    date = c.fetchall()[0][0]
    c.execute('SELECT MAX(altitude) FROM nmea' + str(len(container)-1))
    xHeight = c.fetchall()[0][0]
    c.execute('SELECT MIn(altitude) FROM nmea' + str(len(container) - 1))
    nHeight = c.fetchall()[0][0]
    c.execute('SELECT MAX(speed) FROM nmea' + str(len(container) - 1))
    xSpeed = c.fetchall()[0][0]
    c.execute('SELECT MIN(speed) FROM nmea' + str(len(container) - 1))
    nSpeed = c.fetchall()[0][0]
    c.execute('SELECT MAX(quality) FROM nmea' + str(len(container) - 1))
    quality = c.fetchall()[0][0]
    length=0
    if(quality!=None):
        length = minusTime(aTime, bTime)
    c.execute("INSERT INTO DB VALUES (?,?,?,?,?,?,?,?)", (nameDB, date, length, xSpeed, nSpeed, xHeight, nHeight, quality))
    DBfile.commit()
    DBfile.close()

#catch an ardess of file and open giveName with it
def giveOne():
    adress = askopenfilename()
    giveName(adress)

#catch an ardess of directory and open giveName with all its files
def giveDirectory():
    adress = askdirectory()
    counter = 0
    if os.path.isdir(adress):
        for file in os.listdir(adress):
            suffix=file.split(".")
            if (suffix[-1]=="txt" or suffix[-1]=="nmea"):#check if it's a matched file
                giveName(adress + "/" + file)

#convert the speed
def knots_to_kph(value):
    return "%.2f" % (float(value) * 1.85200)

#takes to times, and find the length between each other
def minusTime(a, b):
    #if(a==None):
     #   return a
    aList = a.split(":")
    bList = b.split(":")
    hower = int(bList[0])-int(aList[0])
    minute = int(bList[1])-int(aList[1])
    if(minute<0):
        hower = hower - 1
        minute = 60 + minute
    second = int(bList[2])-int(aList[2])
    if (second < 0):
        minute = minute - 1
        second = 60 + second
    return str(hower)+":"+str(minute)+":"+str(second)

#match the time for the DB and KML
def format_time(value):
    hour = value[:2]
    minute = value[2:4]
    second = value[4:6]
    time = hour + ":" + minute + ":" + second
    return time

#match the date for the DB and KML
def format_date(value):
    day = value[:2]
    month = value[2:4]
    year = value[4:6]
    date = "20"+year+"-"+month+"-"+day
    return date

#saving all the data in one big CSV file
def toCSV():
    adress=asksaveasfilename()+'.csv'
    with open(adress, 'w') as csvfile:
        fieldnames = ['name', 'time', 'length', 'north', 'wide', 'east', 'quality', 'nos', 'hdop', 'altitude', 'hog', 'speed', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name in container:
            writer.writerows(name)

#saving every data in another KML file
def toKML():
    n=len(container)
    adress = askdirectory()
    for i in range(0, n):
        if(len(container[i])==0):#check if there is info at that file at all
            continue
        skip = 5
        DBfile = sqlite3.connect('temp.db')
        DB = DBfile.execute("SELECT * FROM nmea" + str(i))
        file = adress + '/' + container[i][0]['name'] + '.kml'
        FILE = open(file, 'w')
        FILE.truncate(0)
        FILE.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
        FILE.write('<kml xmlns="http://earth.google.com/kml/2.0">\n')
        FILE.write('    <Document>\n')
        FILE.write('     <Folder>\n')
        FILE.write('     <name>Point Features</name>\n')
        FILE.write('     <description>Point Features</description>\n\n')
        j = 0
        for line in DB:
            if j % skip == 0:
                FILE.write('<Placemark>\n')
                FILE.write('    <TimeStamp>\n')
                FILE.write('     <when>%s%s</when>\n' % (line[12]+"T", line[1])+"Z")
                FILE.write('    </TimeStamp>\n')
                lat = float(line[2][:2]) + (float(line[2][2:]) / 60)
                lon = float(line[4][:3]) + (float(line[4][3:]) / 60)
                FILE.write('    <description><![CDATA[Lat: %s <br> Lon: %s<br> Speed: %s <br>]]></description>\n' % (
                lat, lon, str(line[11])+ " km/h"))
                FILE.write('    <Point>\n')
                FILE.write('        <coordinates>%s,%s,%s</coordinates>\n' % (str(lon), str(lat), line[9]))
                FILE.write('    </Point>\n')
                FILE.write('</Placemark>\n')
                j = j + 1
            else:
                j = j + 1
        FILE.write('        </Folder>\n')
        FILE.write('    </Document>\n')
        FILE.write('</kml>\n')
        FILE.close()
        DBfile.close()

def mesBox():
    tkinter.messagebox.showinfo("About Us:", "Ori Renick\nElyashiv Miller\nYitshak Shapira\nAviad Atlas")

#print the DB table
def SQL1():
    DBfile = sqlite3.connect('temp.db')
    c = DBfile.cursor()
    c.execute('SELECT * FROM DB')
    print(c.fetchall())
    DBfile.commit()
    DBfile.close()

#creats line to enter questions to the SQLite
def SQL2():
    l2.pack()
    #l2.grid(row=1, sticky=E)
    str=""
    def getText():
        str = e1.get()
        DBfile = sqlite3.connect('temp.db')
        c = DBfile.cursor()
        c.execute(str)
        answer = c.fetchall()
        print(answer)
        DBfile.commit()
        DBfile.close()
    e1.pack()
    #e2 = Entry(root)
    #e2.grid(row=0, column=1)
    b = Button(root, text="Enter", width=10, command=getText)
    b.pack()


#main GUI part:
root=Tk()
l1=Label(root, text='wellcome to GPS Pharser')
l1.grid(row=0)
l1.pack()

l2 = Label(root, text="enter question or 1 to exit:")
e1 = Entry(root)

fr1=Frame(root, width=300, height=300)
fr1.pack()

menu=Menu(root)
root.config(menu=menu)

subMenu1=Menu(menu)
menu.add_cascade(label="file", menu=subMenu1)
subMenu1.add_command(label="Open NMEA file", command=giveOne)
subMenu1.add_command(label="Open NMEA class", command=giveDirectory)
subMenu1.add_separator()
subMenu1.add_command(label="Save as CSV", command=toCSV)
subMenu1.add_command(label="Save as KML", command=toKML)
subMenu1.add_separator()
subMenu1.add_command(label="Exit", command=exit)

subMenu2=Menu(menu)
menu.add_cascade(label="SQLite", menu=subMenu2)
subMenu2.add_command(label="Print DB", command=SQL1)
subMenu2.add_command(label="Add to SQLite", command=SQL2)

subMenu3=Menu(menu)
menu.add_cascade(label="help", menu=subMenu3)
subMenu3.add_command(label="About", command=mesBox)

#drop tables of last time
DBfile = sqlite3.connect('temp.db')
c = DBfile.cursor()
c.execute('drop table if exists DB')
DBfile.commit()
DBfile.close()


root.mainloop()