#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
import csv

# File names
temptrains = 'data/temperatetrains.csv'
tempcargo = 'data/temperatecargo.csv'
subtrains = 'data/subarctictrains.csv'
subarcticcargo = 'data/subarcticcargo.csv'
subtropcargo = 'data/subtropicalcargo.csv'
toytrains = 'data/toylandtrains.csv'
toycargo = 'data/toylandcargo.csv'


class Window:
    def __init__(self, master):
        self.master = master

        # Variables
        self.climate = IntVar()
        self.unit = IntVar()
        self.speedpercentage = DoubleVar()
        self.enginecount = IntVar()

        self.speedpercentage.set(1.0)
        self.enginecount.set(1)

        # Labels.
        self.trainlistlabel = ttk.Label(self.master, text='Trains')
        self.carlistlabel =  ttk.Label(self.master, text='Cargo')

        self.trainlengthlabel = ttk.Label(self.master, text='Length = 0 cars\n+ engine', justify='right')
        self.trainweightlabel = ttk.Label(self.master, text='Weight (t)')
        self.trainspeedlabel = ttk.Label(self.master, text='Speed (km/h)')
        self.trainpowerlabel = ttk.Label(self.master, text='Power (kW)')

        self.cargoweightlabel = ttk.Label(self.master, text='Weight (t)')
        self.speedpercentlabel = ttk.Label(self.master, text='% speed 20-100')
        self.trainheadslabel = ttk.Label(self.master, text='No. of engines:')

        # List boxes.
        self.trainlist = Listbox(self.master, yscrollcommand=True, height=10, width=21, exportselection=False)
        self.trainlist.bind('<<ListboxSelect>>', self.trainselect)
        self.trainscroll = ttk.Scrollbar(self.master, orient=VERTICAL, command=self.trainlist.yview)
        self.trainscroll.grid(row=1, column=1, sticky=NS)
        self.trainlist['yscrollcommand'] = self.trainscroll.set

        self.carlist = Listbox(self.master, yscrollcommand=True, height=10, width=21, exportselection=False)
        self.carlist.bind('<<ListboxSelect>>', self.cargoselect)
        self.carscroll = ttk.Scrollbar(self.master, orient=VERTICAL, command=self.carlist.yview)
        self.carscroll.grid(row=1, column=4, sticky=NS)
        self.carlist['yscrollcommand'] = self.carscroll.set


        # Buttons
        calculatebutton = ttk.Button(self.master, text='Calculate', command=self.calculate)

        # Entry boxes.

        self.trainweightentry = ttk.Entry(self.master)
        self.trainspeedentry = ttk.Entry(self.master)
        self.trainpowerentry= ttk.Entry(self.master)

        self.cargoweightentry = ttk.Entry(self.master)

        # Slider.

        self.speedslider = ttk.Scale(self.master, from_=0.2, to=1.0, orient=HORIZONTAL, variable=self.speedpercentage, length=165)

        # Spinbox.

        self.trainenginecountbox = ttk.Spinbox(self.master, from_=1, to=6, increment=1, textvariable=self.enginecount, width=17)

        # Top menu.
        barmenu = Menu(self.master, tearoff=0)
        climatemenu = Menu(barmenu, tearoff=0)
        unitmenu = Menu(barmenu, tearoff=0)

        climatemenu.add_radiobutton(label='Temperate', variable=self.climate, value=0, command=self.selectclimate)
        climatemenu.add_radiobutton(label='Sub-Arctic', variable=self.climate, value=1, command=self.selectclimate)
        climatemenu.add_radiobutton(label='Sub-Tropical', variable=self.climate, value=2, command=self.selectclimate)
        climatemenu.add_radiobutton(label='Toyland', variable=self.climate, value=3, command=self.selectclimate)

        unitmenu.add_radiobutton(label='Metric', variable=self.unit, value=0, command=self.unitselect)
        unitmenu.add_radiobutton(label='Imperial', variable=self.unit, value=1, command=self.unitselect)
        unitmenu.add_radiobutton(label='SI', variable=self.unit, value=2, command=self.unitselect)

        barmenu.add_cascade(label='Climate', menu=climatemenu)
        barmenu.add_cascade(label='Unit', menu=unitmenu)

        self.master.config(menu=barmenu)

        # Placing down train list and values.
        self.trainlistlabel.grid(row=0, column=0,padx=5, pady=5)
        self.trainlist.grid(row=1, column=0, padx=5, pady=5,)
        self.trainweightlabel.grid(row=2, column=0, padx=5, pady=5)
        self.trainweightentry.grid(row=3, column=0, padx=5, pady=5)
        self.trainspeedlabel.grid(row=4, column=0, padx=5, pady=5)
        self.trainspeedentry.grid(row=5, column=0, padx=5, pady=5)
        self.trainpowerlabel.grid(row=6, column=0, padx=5, pady=5)
        self.trainpowerentry.grid(row=7, column=0, padx=5, pady=5)


        # Placing cargo list and value
        self.carlistlabel.grid(row=0, column=2, padx=5, pady=5)
        self.carlist.grid(row=1, column=2, padx=5, pady=5)
        self.cargoweightlabel.grid(row=2, column=2, padx=5, pady=5)
        self.cargoweightentry.grid(row=3, column=2, padx=5, pady=5)
        self.speedpercentlabel.grid(row=4, column=2, padx=5, pady=5)
        self.speedslider.grid(row=5, column=2, padx=5, pady=5)
        self.trainheadslabel.grid(row=6, column=2, padx=5, pady=5)
        self.trainenginecountbox.grid(row=7, column=2, padx=5, pady=5)

        # Placing calculations
        calculatebutton.grid(row=8, column=0, pady=5)
        self.trainlengthlabel.grid(row=8, column=2, pady=5)

        # Filling lists on launch.
        self.selectclimate()

    def trainselect(self, evt):
        newtraincsv = None

        # Check climate and select csv.
        if self.climate.get() == 0:                     # Temperate
            newtraincsv = open(temptrains, newline='', encoding='utf-8')
        elif self.climate.get() == 1:                   # Sub-arctic
            newtraincsv = open(subtrains, newline='', encoding='utf-8')
        elif self.climate.get() == 2:                   # Sub-tropical
            newtraincsv = open(subtrains, newline='', encoding='utf-8')
        elif self.climate.get() == 3:                   # Toyland
            newtraincsv = open(toytrains, newline='', encoding='utf-8')

        # Make list for easy access.
        trainreader = csv.reader(newtraincsv)
        trainselectlist = list(trainreader)

        # Fetch number from list and get numbers.
        newspeed = float(trainselectlist[self.trainlist.curselection()[0]][1])
        newweight = float(trainselectlist[self.trainlist.curselection()[0]][2])
        newpower = float(trainselectlist[self.trainlist.curselection()[0]][3])

        # Convert numbers.
        if self.unit.get() == 0:            # Metric.
            newspeed = round(newspeed * 3.66, 1)
            # Weight is already good.
            # Torque is already good.
        elif self.unit.get() == 1:          # Imperial.
            newspeed = round(newspeed * 2.286, 1)
            newweight = round(newweight * 1.1, 1)
            newpower = round(newpower / 0.74, 1)
        elif self.unit.get() == 2:          # SI
            # Speed is good.
            newweight *= 1000
            # Torque is good.

        # Remove values from entry boxes.
        self.trainspeedentry.delete(0, END)
        self.trainweightentry.delete(0, END)
        self.trainpowerentry.delete(0, END)

        # Put new values in entry boxes.
        self.trainspeedentry.insert(0, newspeed)
        self.trainweightentry.insert(0, newweight)
        self.trainpowerentry.insert(0, newpower)

        # Close opened file.
        newtraincsv.close()


    def cargoselect(self, evt):
        newcarcsv = None

        # Check climate and select csv.
        if self.climate.get() == 0:  # Temperate
            newcarcsv = open(tempcargo, newline='', encoding='utf-8')
        elif self.climate.get() == 1:  # Sub-arctic
            newcarcsv = open(subarcticcargo, newline='', encoding='utf-8')
        elif self.climate.get() == 2:  # Sub-tropical
            newcarcsv = open(subtropcargo, newline='', encoding='utf-8')
        elif self.climate.get() == 3:  # Toyland
            newcarcsv = open(toycargo, newline='', encoding='utf-8')

        # Create list from csv
        newcarcsvreader = csv.reader(newcarcsv)
        csvcarlist = list(newcarcsvreader)

        # Get weight.
        newweight = float(csvcarlist[self.carlist.curselection()[0]][1])

        # Convert and round weight.
        if self.unit.get() == 0:                # Metric
            pass
        elif self.unit.get() == 1:              # Imperial
            newweight = round(newweight * 1.1, 1)
        else:                                   # SI
            newweight *= 1000

        # Put number in entry box.
        self.cargoweightentry.delete(0, END)
        self.cargoweightentry.insert(0, newweight)

        # Close opened file
        newcarcsv.close()

    def selectclimate(self):
        newtraincsv = None
        newcarcsv = None

        # Clear both lists.
        self.trainlist.delete(0, END)
        self.carlist.delete(0, END)

        # Figure out what climate has been chosen.
        if self.climate.get() == 0:             # Temperate
            newtraincsv = open(temptrains, newline='', encoding='utf-8')
            newcarcsv = open(tempcargo, newline='', encoding='utf-8')
        elif self.climate.get() == 1:           # Sub-arctic
            newtraincsv = open(subtrains, newline='', encoding='utf-8')
            newcarcsv = open(subarcticcargo, newline='', encoding='utf-8')
        elif self.climate.get() == 2:           # Sub-tropical
            newtraincsv = open(subtrains, newline='', encoding='utf-8')
            newcarcsv = open(subtropcargo, newline='', encoding='utf-8')
        elif self.climate.get() == 3:           # Toyland
            newtraincsv = open(toytrains, newline='', encoding='utf-8')
            newcarcsv = open(toycargo, newline='', encoding='utf-8')

        # Fill train list.

        traincsvreader = csv.reader(newtraincsv)
        newtrainlist = list(traincsvreader)

        for train in range(len(newtrainlist)):
            self.trainlist.insert(train, newtrainlist[train][0])

        # Fill cargo list

        traincsvreader = csv.reader(newcarcsv)
        newtrainlist = list(traincsvreader)

        for car in range(len(newtrainlist)):
            self.carlist.insert(car, newtrainlist[car][0])

        # Close files
        newtraincsv.close()
        newcarcsv.close()


    def unitselect(self):
        if self.unit.get() == 0:
            self.trainspeedlabel.config(text='Speed (km/h)')
            self.trainpowerlabel.config(text='Power (kW)')
            self.trainweightlabel.config(text='Weight (t)')
            self.cargoweightlabel.config(text='Weight (t)')
        elif self.unit.get() == 1:
            self.trainspeedlabel.config(text='Speed (mph)')
            self.trainpowerlabel.config(text='Power (hp)')
            self.trainweightlabel.config(text='Weight (t)')
            self.cargoweightlabel.config(text='Weight (t)')
        elif self.unit.get() == 2:
            self.trainspeedlabel.config(text='Speed (m/s)')
            self.trainpowerlabel.config(text='Power (kW)')
            self.trainweightlabel.config(text='Weight (kg)')
            self.cargoweightlabel.config(text='Weight (kg)')


    def calculate(self):
        try:
            # Remove commas from strings
            calctrainweight = float(self.trainweightentry.get().replace(',', ''))
            calccargoweight = float(self.cargoweightentry.get().replace(',', ''))
            calcspeed = float(self.trainspeedentry.get().replace(',', ''))
            calcpower = float(self.trainpowerentry.get().replace(',', ''))

            # Converting units.
            if self.unit.get() == 0:        # Metric
                # Weights are already good
                calcspeed /= 3.66
                calcpower *= 1000
            elif self.unit.get() == 1:      # Imperial
                calctrainweight /= 1.1
                calccargoweight /= 1.1
                calcspeed /= 2.286
                calcpower *= 746.67
            else:                           # SI
                calctrainweight /= 1000
                calccargoweight /= 1000
                # Speed already good
                calcpower *= 1000

            finalnumber = int((calcpower * self.enginecount.get() - calctrainweight *
                               self.enginecount.get() * 35 * calcspeed * self.speedpercentage.get()) /
                              (calccargoweight * 35 * calcspeed * self.speedpercentage.get()))
            self.trainlengthlabel.config(text=f'Length = {finalnumber} cars\n+ engine')
        except ValueError:
            self.trainlengthlabel.config(text='Error! Values in \nboxes must be numbers!')



root = Tk()
root.geometry('200x150')
root.minsize(400, 480)
root.maxsize(400, 480)
root.title('OpenTTD Train Length Calculator')

window = Window(root)
root.mainloop()
