import tkinter
from tkinter import ttk
import os
import pickle


#  Device class
class Device:
    def __init__(self, indexnumber, devicename):
        self.indexnumber = indexnumber
        self.devicename = devicename


class DeviceSaveFile:       # Used to save files, and for program to remember what the last sink user used is.
    def __init__(self):
        self.devicelist = devicelist
        self.selecteddevice = selecteddevice


#  Global variables
devicelist= []
selecteddevice = Device('1', 'Placeholder device name')
home = os.path.expanduser('~') + '/.QSS'

#  Tkinter objects
root = tkinter.Tk()


#  Methods
def changedefaultsink():        # Will use terminal to change default sink device in Pulseaudio
    os.system('pacmd set-default-sink ' + selecteddevice.indexnumber)


def savedevices():              # Save list of devices to file in computer.
    file = open('devices', 'wb')
    savefile = DeviceSaveFile()
    pickle.dump(savefile, file)
    file.close()


def loaddevices():
    if not os.path.exists(home):
        os.mkdir(home)
    os.chdir(home)
    try:
        global devicelist
        global selecteddevice
        file = open('devices', mode='rb')
        devicesavefile = pickle.load(file)
        devicelist = devicesavefile.devicelist
        selecteddevice = devicesavefile.selecteddevice
        changedefaultsink()
        file.close()
    except OSError:
        print('OSError, could not read the devices list.')

#  Window
class MainWindow:
    def __init__(self, root):
        self.root = root
        root.geometry("250x298")
        root.minsize(250, 298)
        root.protocol("WM_DELETE_WINDOW", self.closeprogram)

        #  Frame
        mainframe = ttk.Frame(root)

        #  Listbox
        self.indexselectionbox = tkinter.Listbox(mainframe, selectmode=tkinter.SINGLE, width=30)

        #  Label
        deviceselecttext = ttk.Label(mainframe, text='Select device:')
        self.currentselectionvariable = tkinter.StringVar(value=selecteddevice.devicename)
        currentselectionlabel = ttk.Label(mainframe, textvariable=self.currentselectionvariable)

        #  Button
        setsinkbutton = ttk.Button(mainframe, text='Set sink', command=self.setsink)

        #  Top bar menu
        menu = tkinter.Menu(root)
        menu.add_command(label='Add', command=self.addsink)
        menu.add_command(label='Delete', command=self.deletesink)
        menu.add_command(label='Save', command=savedevices)

        #  Packing
        root.config(menu=menu)

        mainframe.pack()
        deviceselecttext.pack(padx=5, pady=5)
        self.indexselectionbox.pack(padx=5, pady=5)
        currentselectionlabel.pack(padx=5, pady=5)
        setsinkbutton.pack(padx=5, pady=5)

        self.refreshlist()

    def refreshlist(self):                              # Deletes listbox list and creates new one.
        self.indexselectionbox.delete(0, tkinter.END)
        for i in devicelist:
            self.indexselectionbox.insert(tkinter.END, i.devicename)

    def setsink(self):
        global selecteddevice
        selecteddevice = devicelist[self.indexselectionbox.curselection()[0]]
        self.currentselectionvariable.set(selecteddevice.devicename)
        changedefaultsink()

    def addsink(self):
        toplevel = tkinter.Toplevel(root)
        toplevel.title('Add new device')
        topwindow = CreateWindow(toplevel, self)

    def deletesink(self):                               # Delete selected device from list
        global devicelist
        devicelist.pop(self.indexselectionbox.curselection()[0])
        self.refreshlist()

    def closeprogram(self):
        savedevices()
        self.root.destroy()


class CreateWindow:
    def __init__(self, toplevel, parentwindow):
        self.parentwindow = parentwindow
        self.toplevel = toplevel
        toplevel.geometry('250x160')
        toplevel.minsize(250, 160)
        # Labels
        devicenamelabel = ttk.Label(toplevel, text='Enter device name:')
        deviceindexlabel = ttk.Label(toplevel, text='Enter name from pacmd sink-lists:')

        # Entry box
        self.devicenamebox = ttk.Entry(toplevel, width=30)
        self.deviceindexbox = ttk.Entry(toplevel, width=30)

        # Button

        createdevicebutton = ttk.Button(toplevel, text='Add device', command=self.adddevice)

        # Packing
        devicenamelabel.pack(padx=5, pady=5)
        self.devicenamebox.pack(padx=5, pady=5)
        deviceindexlabel.pack(padx=5, pady=5)
        self.deviceindexbox.pack(padx=5, pady=5)
        createdevicebutton.pack(padx=5, pady=5)

    def adddevice(self):
        global devicelist
        devicelist.append(Device(self.deviceindexbox.get(), self.devicenamebox.get()))
        self.parentwindow.refreshlist()
        self.toplevel.destroy()


loaddevices()
root.title('Quick Sink Switch')
mainwindow = MainWindow(root)
root.mainloop()
