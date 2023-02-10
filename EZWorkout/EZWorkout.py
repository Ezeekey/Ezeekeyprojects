#!/usr/bin/env python3

import tkinter
from tkinter import ttk
import pickle
import time
import os
import threading
import platform

version = 'v1.0.2'

class Set:
    def __init__(self):
        self.name = 'untitled'
        self.exercises = [('none', '0 lbs', '0')]

class Exercise:
    def __init__(self):
        self.set = Set()
        self.currentnumber = 0
        self.completesets = 0
        self.filename = 'untitled'

    def setweight(self, newweight):
        exercise = self.set.exercises[self.currentnumber]
        self.set.exercises[self.currentnumber] = (exercise[0], newweight, exercise[2])

    def nextexercise(self):
        self.currentnumber += 1
        if self.currentnumber >= len(self.set.exercises):
            self.currentnumber = 0
            self.completesets += 1

    def reset(self):
        self.currentnumber = 0
        self.completesets = 0


class MainExerciseWindow:
    def __init__(self, root):

        # Frames

        topframe = ttk.Frame(root)
        rightframe = ttk.Frame(root)
        bottomframe = ttk.Frame(root)
        leftframe  = ttk.Frame(root)

        # labels

        self.setnamelabel = ttk.Label(topframe, text='Program name')
        self.exercisenamelabel = ttk.Label(leftframe, text='Set name')
        self.weightlabel = ttk.Label(leftframe, text='Weight')
        self.replabel = ttk.Label(leftframe, text='Reps')
        self.exercisenumberlabel = ttk.Label(leftframe, text='Set 0/0')
        self.setnumberlabel = ttk.Label(leftframe, text='Circuits complete : 0')
        timeelapsedlabel = ttk.Label(bottomframe, text='Time elapsed')
        self.stopwatchlabel = ttk.Label(bottomframe, text='0:00')

        # Buttons

        self.nextbutton = ttk.Button(rightframe, text='Next', command=self.nextexercise, state=tkinter.DISABLED)
        self.setweightbutton = ttk.Button(rightframe, text='Set weight', state=tkinter.DISABLED, command=self.setweight)
        self.donebutton = ttk.Button(bottomframe, text='Start', command=self.startstop)

        # Entry box

        self.weightvar = tkinter.StringVar()
        self.weightbox = ttk.Entry(rightframe, textvariable=self.weightvar, state=tkinter.DISABLED)

        # Menu bar

        self.menubar = tkinter.Menu(root)
        self.menubar.add_command(label='Programs', command=self.opensetwindow)
        self.menubar.add_command(label='About', command=self.about)
        root.config(menu=self.menubar)

        # Packing top

        topframe.pack(side=tkinter.TOP)
        self.setnamelabel.pack()

        # Packing right

        rightframe.pack(side=tkinter.RIGHT)
        self.nextbutton.pack(pady=5, padx=5)
        self.weightbox.pack(padx=5)
        self.setweightbutton.pack(padx=5)

        # Packing bottom

        bottomframe.pack(side=tkinter.BOTTOM, pady=5)
        timeelapsedlabel.pack()
        self.stopwatchlabel.pack()
        self.donebutton.pack()

        # Packing left

        leftframe.pack(side=tkinter.LEFT, padx=5)
        self.exercisenamelabel.pack()
        self.weightlabel.pack()
        self.replabel.pack()
        self.exercisenumberlabel.pack()
        self.setnumberlabel.pack()


    def setweight(self):
        global currentset
        currentset.setweight(self.weightbox.get())
        self.weightlabel.config(text=f'Weight : {currentset.set.exercises[currentset.currentnumber][1]}')

    def nextexercise(self):
        global currentset
        currentset.nextexercise()
        self.displayexercise()
        self.weightvar.set('')

    def displayexercise(self):
        global currentset
        newexercise = currentset.set.exercises[currentset.currentnumber]
        self.exercisenamelabel.config(text=newexercise[0])
        self.weightlabel.config(text=f'Weight : {newexercise[1]}')
        self.replabel.config(text=f'Reps : {newexercise[2]}')
        self.exercisenumberlabel.config(text=f'Set {currentset.currentnumber + 1}/{len(currentset.set.exercises)}')
        self.setnumberlabel.config(text=f'Circuits complete : {currentset.completesets}')

    def startstop(self):
        global exerciseon
        if not exerciseon:          # Start exercise program.
            # Start set from beginning
            exerciseon = True
            currentset.reset()

            # Threading for stopwatch
            timedisplaythread = threading.Thread(target=self.displaytime)
            timedisplaythread.start()
            timethread = threading.Thread(target=stopwatch_start)
            timethread.start()

            # Turn start to done..
            self.donebutton.config(text='Done')

            # Turning on buttons on right.
            self.nextbutton.config(state=tkinter.NORMAL)
            self.setweightbutton.config(state=tkinter.NORMAL)
            self.weightbox.config(state=tkinter.NORMAL)
            self.weightvar.set('')

            # Check if empty exercise
            if len(currentset.set.exercises) == 0:
                currentset.set.exercises.append(('none', '0 lbs', '0'))

            # Set text on left to display exercise.
            self.displayexercise()
            self.setnamelabel.config(text=currentset.set.name)
        else:                       # Stop exercise program.
            # Kill threads.
            exerciseon = False

            # Turn done to start.
            self.donebutton.config(text='Start')

            # Disable buttons on right.
            self.nextbutton.config(state=tkinter.DISABLED)
            self.setweightbutton.config(state=tkinter.DISABLED)
            self.weightbox.config(state=tkinter.DISABLED)
            self.weightvar.set('')

            # Save workout
            saveworkout()

    def displaytime(self):
        global starttime
        global currenttime

        while exerciseon:
            seconds = currenttime - starttime
            minutes = int(seconds / 60)
            seconds -= minutes * 60

            self.stopwatchlabel.config(text=f'{minutes}:{seconds:02d}')

            time.sleep(0.1)

    def opensetwindow(self):
        global exerciseon

        # Open the window.
        setwindow = SetSelectWindow(root)

        # Deactivate the buttons on main exercise window.
        self.deactivate()

    def deactivate(self):
        # Deactivate the buttons on main exercise window.
        exerciseon = False
        self.nextbutton.config(state=tkinter.DISABLED)
        self.setweightbutton.config(state=tkinter.DISABLED)
        self.weightbox.config(state=tkinter.DISABLED)
        self.weightvar.set('')
        self.donebutton.config(text='Start', state=tkinter.DISABLED)
        self.menubar.entryconfig('Programs', state=tkinter.DISABLED)
        self.menubar.entryconfig('About', state=tkinter.DISABLED)

    def reactivate(self):
        self.donebutton.config(state=tkinter.NORMAL)
        self.menubar.entryconfig('Programs', state=tkinter.NORMAL)
        self.menubar.entryconfig('About', state=tkinter.NORMAL)

    def about(self):
        # Deactivate the main window.
        self.deactivate()

        def close():
            self.reactivate()
            aboutwin.destroy()

        aboutwin = tkinter.Toplevel(root)
        aboutwin.minsize(400, 180)
        aboutwin.protocol('WM_DELETE_WINDOW', close)

        # Labels.
        mainlabel = ttk.Label(aboutwin, text=f'EZWorkout. A free and simple workout planning application'
                                             '\nWritten by Ezekiel Taves - 10/17/2022'
                                             f'\n\n{version}')
        cautionlabel = ttk.Label(aboutwin, text='Caution!\nThe .set files are pickle files, and not secure.\n'
                                                'Only use sets from trusted sources!')

        # Packing
        mainlabel.pack(side=tkinter.TOP, pady=10)
        cautionlabel.pack(side=tkinter.BOTTOM, pady=10)

class SetSelectWindow:
    def __init__(self, root):
        self.setwin = tkinter.Toplevel(root)
        self.setwin.protocol('WM_DELETE_WINDOW', self.closewindow)
        self.setwin.title('Select program')
        self.setwin.minsize(259, 254)
        self.setwin.maxsize(259, 254)

        # Entry box
        self.setentrybox = tkinter.Listbox(self.setwin, width=30)
        self.setscrollbar = ttk.Scrollbar(self.setwin, command=self.setentrybox.yview)
        self.setentrybox['yscrollcommand'] = self.setscrollbar.set

        # Button
        self.selectbutton = ttk.Button(self.setwin, text='Select', command=self.selectexercise)

        # Menu
        self.menu = tkinter.Menu(self.setwin)
        self.menu.add_command(label='New', command=self.createnewset)
        self.menu.add_command(label='Edit', command=self.editset)
        self.menu.add_command(label='Delete', command=self.deleteset)

        # Packing
        self.setentrybox.grid(column=0,row=0, sticky=tkinter.NS)
        self.selectbutton.grid(column=0, row=1, pady=5, sticky=tkinter.N)
        self.setscrollbar.grid(column=1, row=0, sticky=tkinter.NS)
        self.setwin.config(menu=self.menu)

        # Set the list up.
        self.refreshlist()

    def closewindow(self):
        window.reactivate()
        self.setwin.destroy()

    def selectexercise(self):
        # Load selected exercise
        loadworkout(self.setentrybox.get(self.setentrybox.curselection()[0]))

        # Close window
        self.closewindow()

    def refreshlist(self):
        # Clear list box.
        self.setentrybox.delete(0, tkinter.END)

        # Get items for list.
        setlist = []

        for i in os.listdir('sets'):
            splitstring = i.rpartition('.')
            if splitstring[2] == 'set':
                setlist.append(splitstring[0])

        # Alphabetically sort list.
        setlist.sort(key=str.lower)

        # Add names from folder to list box
        for i in setlist:
            self.setentrybox.insert(tkinter.END, i)

    def createnewset(self):
        # Create a blank workout
        currentset.set = Set()
        currentset.filename = 'untitled'

        # Open new set window.
        self.opensetwindow()

    def editset(self):
        # Load selected workout.
        loadworkout(self.setentrybox.get(self.setentrybox.curselection()[0]))

        # Open new set window.
        self.opensetwindow()

    def opensetwindow(self):
        # Deactivate this window before opening new set window.
        self.deactivate()

        # Open new set window.
        editwindow = NewSetWindow(root, self)

    def deleteset(self):
        # Get index of selection
        try:
            indexeditem = self.setentrybox.curselection()[0]
            self.deactivate()

            # Prompt
            deletewin = tkinter.Toplevel(root)

            def destroydeletewindow():
                self.reactivate()
                deletewin.destroy()

            def yes():
                os.remove('sets/' + self.setentrybox.get(indexeditem) + '.set')
                destroydeletewindow()
                self.refreshlist()

            def no():
                destroydeletewindow()

            deletewin.protocol('WM_DELETE_WINDOW', destroydeletewindow)

            # Label.
            promptlabel = ttk.Label(deletewin,
                                    text=f'Are you sure you want to delete {self.setentrybox.get(indexeditem)}?')

            # Buttons
            yesbutton = ttk.Button(deletewin, text='Yes', command=yes)
            nobutton = ttk.Button(deletewin, text='No', command=no)

            # Packing.
            promptlabel.pack(side=tkinter.TOP, padx=10, pady=10)
            yesbutton.pack(side=tkinter.RIGHT, padx=10, pady=10)
            nobutton.pack(side=tkinter.LEFT, padx=10, pady=10)
        except:
            self.reactivate()

    def deactivate(self):
        self.menu.entryconfig('New', state=tkinter.DISABLED)
        self.menu.entryconfig('Edit', state=tkinter.DISABLED)
        self.menu.entryconfig('Delete', state=tkinter.DISABLED)
        self.selectbutton.config(state=tkinter.DISABLED)
        self.setentrybox.config(state=tkinter.DISABLED)

    def reactivate(self):
        self.menu.entryconfig('New', state=tkinter.NORMAL)
        self.menu.entryconfig('Edit', state=tkinter.NORMAL)
        self.menu.entryconfig('Delete', state=tkinter.NORMAL)
        self.selectbutton.config(state=tkinter.NORMAL)
        self.setentrybox.config(state=tkinter.NORMAL)
        self.refreshlist()


class NewSetWindow:
    def __init__(self, root, setwindow):
        # Initiating the window.
        self.editwin = tkinter.Toplevel(root)
        self.editwin.title(f'{currentset.filename}.set')
        self.editwin.minsize(350, 370)

        def closewindow():
            try:
                setwindow.reactivate()
            except tkinter.TclError:
                print('Could not find program menu when closing.')
            finally:
                self.editwin.destroy()

        self.editwin.protocol('WM_DELETE_WINDOW', closewindow)

        # Frames
        topframe = ttk.Frame(self.editwin)
        rightframe = ttk.Frame(self.editwin)
        leftframe = ttk.Frame(self.editwin)

        # Entry boxes
        self.setnamestring = tkinter.StringVar()
        self.setnamestring.set(currentset.set.name)
        self.setnamebox = ttk.Entry(topframe, textvariable=self.setnamestring)
        self.exercisenamevar = tkinter.StringVar()
        self.exercisenamebox = ttk.Entry(rightframe, textvariable=self.exercisenamevar)
        self.weightvar = tkinter.StringVar()
        self.weightbox = ttk.Entry(rightframe, textvariable=self.weightvar)
        self.repvar = tkinter.StringVar()
        self.repbox = ttk.Entry(rightframe, textvariable=self.repvar, validate='key')

        # Labels
        self.setnamelabel = ttk.Label(topframe, text='Program title')
        self.exercisenamelabel = ttk.Label(rightframe, text='Set name')
        self.weightlabel = ttk.Label(rightframe, text='Weight')
        self.replabel = ttk.Label(rightframe, text='Reps')
        self.savedlabel = ttk.Label(rightframe, text='')

        # Buttons.
        self.newexercisebutton = ttk.Button(leftframe, text='New set.', command=self.newexercise)
        self.deleteexercisebutton = ttk.Button(leftframe, text='Delete set', command=self.deleteexercise)
        self.setexercisebutton = ttk.Button(rightframe, text='Set set', command=self.editexercise)

        # Menu.
        self.menu = tkinter.Menu(self.editwin)
        self.menu.add_command(label='Save', command=self.save)
        self.menu.add_command(label='Save as', command=self.saveas)
        self.menu.add_command(label='Clear', command=self.clear)
        self.editwin.config(menu=self.menu)

        # Listbox
        self.exerciselist = tkinter.Listbox(leftframe, selectmode=tkinter.SINGLE, exportselection=False)
        self.exerciselist.bind('<<ListboxSelect>>', self.selectexercise)

        # Packing.

        # Top.
        topframe.pack(side=tkinter.TOP)
        self.setnamelabel.pack(pady=5)
        self.setnamebox.pack(pady=5)

        # Right
        rightframe.pack(side=tkinter.RIGHT)
        self.exercisenamelabel.pack(padx=5, pady=5)
        self.exercisenamebox.pack(padx=5, pady=5)
        self.weightlabel.pack(padx=5, pady=5)
        self.weightbox.pack(padx=5, pady=5)
        self.replabel.pack(padx=5, pady=5)
        self.repbox.pack(padx=5, pady=5)
        self.setexercisebutton.pack(padx=5, pady=5)
        self.savedlabel.pack(padx=5, pady=5)

        # Left
        leftframe.pack(side=tkinter.LEFT)
        self.exerciselist.pack(padx=5, pady=5)
        self.newexercisebutton.pack(padx=5, pady=5)
        self.deleteexercisebutton.pack(padx=5, pady=5)

        # Refresh list.
        self.refreshlist()

    def newexercise(self):
        currentset.set.exercises.append(('none', '0 lbs', '0'))
        self.refreshlist()
        self.exerciselist.selection_set(tkinter.END)

    def deleteexercise(self):
        currentset.set.exercises.pop(self.exerciselist.curselection()[0])
        self.refreshlist()

    def save(self):
        # Check if the file is actually new by checking if it is untitled.
        if currentset.filename == 'untitled':
            self.saveas()                       # For naming.
        else:
            currentset.set.name = self.setnamestring.get()
            saveworkout()
            self.saved()
    def saveas(self):
        # Deactivate buttons
        self.deactivate()

        def close():
            self.reactivate()
            dialogwin.destroy()

        def save():
            currentset.filename = filenamebox.get()
            currentset.set.name = self.setnamestring.get()
            saveworkout()
            self.editwin.title(f'{currentset.filename}.set')
            self.saved()
            dialogwin.destroy()

        # Bring up a dialog asking the desired filename.
        dialogwin = tkinter.Toplevel(root)
        dialogwin.protocol('WM_DELETE_WINDOW', close)
        dialogwin.minsize(250, 100)

        # Entry box
        filenamebox = ttk.Entry(dialogwin)

        # Buttons
        cancelbutton = ttk.Button(dialogwin, text='Cancel', command=close)
        savebutton = ttk.Button(dialogwin, text='Save', command=save)

        # Label
        dialoglabel = ttk.Label(dialogwin, text='Please enter a filename for your set.')

        # Packing
        dialoglabel.pack(side=tkinter.TOP, pady=5, padx=5)
        filenamebox.pack(side=tkinter.TOP, pady=5)

        savebutton.pack(side=tkinter.RIGHT, padx=5, pady=5)
        cancelbutton.pack(side=tkinter.LEFT, padx=5, pady=5)

    def saved(self):
        self.deactivate()
        savebox = tkinter.Toplevel(root)
        savelabel = ttk.Label(savebox, text='Saved!')

        def close():
            self.reactivate()
            savebox.destroy()

        savebox.protocol('WM_DELETE_WINDOW', close)

        savelabel.pack(padx=5, pady=5)

    def clear(self):
        # Clear set
        currentset.set.exercises.clear()

        # Refresh list
        self.refreshlist()

    def selectexercise(self, event):
        exercise = currentset.set.exercises[self.exerciselist.curselection()[0]]
        self.exercisenamevar.set(exercise[0])
        self.weightvar.set(exercise[1])
        self.repvar.set(exercise[2])
        self.savedlabel.config(text='')

    def editexercise(self):
        currentset.set.exercises[self.exerciselist.curselection()[0]] = (self.exercisenamevar.get(),
                                                                         self.weightvar.get(),
                                                                         self.repvar.get())
        self.refreshlist()
        self.savedlabel.config(text='saved')

    def refreshlist(self):
        # Clear list
        self.exerciselist.delete(0, tkinter.END)

        # Create new listbox list from exercise list
        for i in currentset.set.exercises:
            self.exerciselist.insert(tkinter.END, i[0])

    def deactivate(self):
        # Deactivate all menu buttons for when save as dialog is up.
        self.menu.entryconfig('Save', state=tkinter.DISABLED)
        self.menu.entryconfig('Save as', state=tkinter.DISABLED)
        self.menu.entryconfig('Clear', state=tkinter.DISABLED)
        self.setnamebox.config(state=tkinter.DISABLED)
        self.exercisenamebox.config(state=tkinter.DISABLED)
        self.weightbox.config(state=tkinter.DISABLED)
        self.repbox.config(state=tkinter.DISABLED)
        self.exerciselist.config(state=tkinter.DISABLED)
        self.newexercisebutton.config(state=tkinter.DISABLED)
        self.deleteexercisebutton.config(state=tkinter.DISABLED)

    def reactivate(self):
        # Reactivate all menu buttons for when save as dialog is closed.
        self.menu.entryconfig('Save', state=tkinter.NORMAL)
        self.menu.entryconfig('Save as', state=tkinter.NORMAL)
        self.menu.entryconfig('Clear', state=tkinter.NORMAL)
        self.setnamebox.config(state=tkinter.NORMAL)
        self.exercisenamebox.config(state=tkinter.NORMAL)
        self.weightbox.config(state=tkinter.NORMAL)
        self.repbox.config(state=tkinter.NORMAL)
        self.exerciselist.config(state=tkinter.NORMAL)
        self.newexercisebutton.config(state=tkinter.NORMAL)
        self.deleteexercisebutton.config(state=tkinter.NORMAL)


def stopwatch_start():
    global starttime
    global currenttime
    starttime = int(time.time())

    while exerciseon:
        currenttime = int(time.time())
        time.sleep(0.1)


def stopprogram():
    global exerciseon
    exerciseon = False
    root.destroy()


def saveworkout():
    # Saves just the list of exercises, and name of workout.
    savefile = open('sets/' + currentset.filename + '.set', mode='wb')
    pickle.dump(currentset.set, savefile)
    savefile.close()


def loadworkout(filename):
    # Load the list of exercises, and name of set.
    loadfile = open('sets/' + filename + '.set', mode='rb')
    currentset.set = pickle.load(loadfile)
    loadfile.close()
    currentset.filename = filename

def fart():
    fartthread = threading.Thread(target=realfart)
    fartthread.start()

def realfart():
    os.system('mpg123 worth.mp3')


# Variables for getting filepath
home = os.path.expanduser('~')
usersystem = platform.system()

if usersystem == 'Windows':         # User is using windows. Put files here.
    if not os.path.exists(home + '/Documents/ezworkouts'):
        os.mkdir(home + '/Documents/ezworkouts')
        os.mkdir(home + '/Documents/ezworkouts/sets')
    os.chdir(home + '/Documents/ezworkouts')
elif usersystem == 'Linux':         # User is using Linux.
    if not os.path.exists(home + '/.ezworkouts'):
        os.mkdir(home + '/.ezworkouts')
        os.mkdir(home + '/.ezworkouts/sets')
    os.chdir(home + '/.ezworkouts')
elif usersystem == 'Darwin':        # User is using Mac
    if not os.path.exists(home + '/Library/Application Support/ezworkouts'):
        os.mkdir(home + '/Library/Application Support/ezworkouts')
        os.mkdir(home + '/Library/Application Support/ezworkouts/sets')
    os.chdir(home + '/Library/Application Support/ezworkouts')

# Delete filepath variables because they are not needed anymore
del(home, usersystem)

currentset = Exercise()
exerciseon = False

starttime = int(time.time())                    # Time when exercise started.
currenttime = int(time.time())                  # Time now after exercise starts.

root = tkinter.Tk()
root.geometry('400x260')
root.minsize(400, 270)
root.title(f'EZWorkouts {version}')
root.protocol('WM_DELETE_WINDOW', stopprogram)
window = MainExerciseWindow(root)

root.mainloop()
