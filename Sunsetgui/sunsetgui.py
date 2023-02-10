#!/usr/bin/env python3

import tkinter
from tkinter import ttk
import datetime
import time
import os
import threading
import pickle


# Global variables

home = os.path.expanduser('~') + '/.sunsetgui'

root = tkinter.Tk()
root.geometry('500x200')
root.minsize(500, 200)
root.title('Sunset GUI v1.1')

sunseton = False                                    # Controls whether the temperature thread is working.
threadon = True                                     # Controls if the thread is alive.

DAY_TEMPERATURE = 6500
night_temperatureint = tkinter.IntVar()        # Color temperature at night time.
night_temperatureint.set(4500)
transition_timeint = tkinter.IntVar()            # Minutes it takes to transition temperature from day to night
transition_timeint.set(60)
dawn_timeint = tkinter.IntVar()                   # Hour, in 24 hour time, that day starts.
dawn_timeint.set(8)
dusk_timeint = tkinter.IntVar()                  # Hour, in 24 hour time, that night starts.
dusk_timeint.set(20)


# Functions

def check_time():                               # Does math using time to figure out the temperature

    dawn_time = datetime.time(hour=dawn_timeint.get())
    dusk_time = datetime.time(hour=dusk_timeint.get())
    now = datetime.datetime.now()
    nowdelta = datetime.timedelta(seconds=now.second, minutes=now.minute, hours=now.hour).total_seconds()

    if now.hour == dawn_time.hour:                                              # Dawn
        # Determine time when screen will start transitioning.
        transitiondelta = datetime.timedelta(hours=dawn_time.hour, minutes=60-transition_timeint.get()).total_seconds()

        # Find slope
        slope = (DAY_TEMPERATURE - night_temperatureint.get()) / (60 * transition_timeint.get())

        # Check if after transition time.
        if nowdelta > transitiondelta:
            nowdelta -= transitiondelta
            return nowdelta * slope + night_temperatureint.get()

        # Not transitioning and still night.
        return night_temperatureint.get()

    elif now.hour == dusk_time.hour:                                            # Dusk
        # Determine time when screen will start transitioning.
        transitiondelta = datetime.timedelta(hours=dusk_time.hour,
                                             minutes=transition_timeint.get()).total_seconds()
        duskdelta = datetime.timedelta(hours=dusk_time.hour).total_seconds()

        # Find slope
        slope = (night_temperatureint.get() - DAY_TEMPERATURE) / (60 * transition_timeint.get())

        # Check if before transition time.
        if nowdelta < transitiondelta:
            nowdelta -= duskdelta
            return nowdelta * slope + DAY_TEMPERATURE

        # Already transitioned to night.
        return night_temperatureint.get()
    elif dawn_time.hour < now.hour < dusk_time.hour:                            # Day
        return DAY_TEMPERATURE
    elif dusk_time.hour < now.hour < dawn_time.hour:                            # Reverse day
        return night_temperatureint.get()
    elif now.hour < dawn_time.hour < dusk_time.hour:                            # Night morning
        return night_temperatureint.get()
    elif now.hour < dusk_time.hour < dawn_time.hour:                            # Reverse night morning
        return DAY_TEMPERATURE
    elif dawn_time.hour < dusk_time.hour < now.hour:                            # Night
        return night_temperatureint.get()
    elif dusk_time.hour < dawn_time.hour < now.hour:                            # Reverse night
        return DAY_TEMPERATURE


def adjust_temperature():                       # Change screen temperature
    os.system(f'redshift -O {check_time()} -P')


def temperature_loop():
    global sunseton
    while threadon:
        save_settings()
        if sunseton:
            adjust_temperature()
        time.sleep(1)


def cancel_loop():
    global sunseton
    sunseton = False
    os.system('redshift -x')


def save_settings():
    file = open('config', mode='wb')
    settings = (night_temperatureint.get(), transition_timeint.get(), dawn_timeint.get(), dusk_timeint.get())
    pickle.dump(settings, file)
    file.close()


def load_settings():
    if not os.path.exists(home):            # On fresh launch when there is no such file.
        os.mkdir(home)
    os.chdir(home)

    try:
        file = open('config', mode='rb')        # Try to read the config file.
        setting = pickle.load(file)
        night_temperatureint.set(setting[0])
        transition_timeint.set(setting[1])
        dawn_timeint.set(setting[2])
        dusk_timeint.set(setting[3])
        file.close()
    except:                                                 # Something went wrong. Set all variables to defaults.
        night_temperatureint.set(4500)
        transition_timeint.set(60)
        dawn_timeint.set(8)
        dusk_timeint.set(20)


# Window

class Window:

    def __init__(self, oroot):
        self.root = oroot

        leftframe = ttk.Frame(self.root)
        rightframe = ttk.Frame(self.root)

        leftframe.pack(side=tkinter.LEFT)
        rightframe.pack(side=tkinter.RIGHT)

        # Sliders
        self.dawn_slider = ttk.Scale(rightframe, from_=0, to=23, variable=dawn_timeint,
                                     command=self.dawnlabelchange, length=200)
        self.dusk_slider = ttk.Scale(rightframe, from_=0, to=23, variable=dusk_timeint,
                                     command=self.dusklabelchange, length=200)
        self.temp_slider = ttk.Scale(leftframe, from_=2700, to=6500, variable=night_temperatureint,
                                     command=self.templabelchange, length=200)
        self.transition_slider = ttk.Scale(leftframe, from_=0, to=60, variable=transition_timeint,
                                           command=self.transitionlabelchange, length=200)

        # Button

        self.startstopbutton = ttk.Button(self.root, text='Start', command=self.startstop)

        # Labels

        self.dawn_label = ttk.Label(rightframe, text=f'Dawn : {dawn_timeint.get()}:00')
        self.dusk_label = ttk.Label(rightframe, text=f'Dusk : {dusk_timeint.get()}:00')
        self.temperature_label = ttk.Label(leftframe, text=f'Temperature : {night_temperatureint.get()}K')
        self.transition_label = ttk.Label(leftframe, text=f'Transition : {transition_timeint.get()} minutes')

        # Placing everything

        self.temperature_label.pack(padx=5, pady=5)
        self.temp_slider.pack(padx=5, pady=5)
        self.transition_label.pack(padx=5, pady=5)
        self.transition_slider.pack(padx=5, pady=5)

        self.dawn_label.pack(padx=5, pady=5)
        self.dawn_slider.pack(padx=5, pady=5)
        self.dusk_label.pack(padx=5, pady=5)
        self.dusk_slider.pack(padx=5, pady=5)

        self.startstopbutton.pack(side=tkinter.BOTTOM, pady=5)

        self.startstop()

    # Methods for UI

    def startstop(self):
        global sunseton

        if not sunseton:
            sunseton = True
            self.startstopbutton.configure(text='Stop')
            adjust_temperature()
        else:
            sunseton = False
            self.startstopbutton.configure(text='Start')
            cancel_loop()

    def dawnlabelchange(self, event):
        self.dawn_label.configure(text=f'Dawn : {dawn_timeint.get()}:00')

    def dusklabelchange(self, event):
        self.dusk_label.configure(text=f'Dusk : {dusk_timeint.get()}:00')

    def templabelchange(self, event):
        self.temperature_label.configure(text=f'Temperature : {night_temperatureint.get()}K')

    def transitionlabelchange(self, event):
        self.transition_label.configure(text=f'Transition : {transition_timeint.get()} minutes')


# Thread handling
temperature_thread = threading.Thread(target=temperature_loop)
temperature_thread.start()


def destroy_thread():
    global threadon
    threadon = False
    cancel_loop()
    root.destroy()


# Get settings.
load_settings()

# Create window.
root.protocol('WM_DELETE_WINDOW', destroy_thread)
window = Window(root)
root.mainloop()
