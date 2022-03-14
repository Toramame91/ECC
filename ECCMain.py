import io
import json
import tkinter as tk
from datetime import datetime
from urllib.request import urlopen
import time
import requests
from PIL import ImageTk, Image

from ItemNode import *
from Clocks import *


def navBarDisplay(_frame):
    # create title bar for navigation menu
    frame = _frame

    whiteBarDisplay = tk.Label(frame, text="__________________________________", bg='#443E3E', fg='white')
    ntDisplay = tk.Label(frame, text="Quick Access", bg='#443E3E', fg='white')
    ntDisplay.grid(row=0, column=0, sticky=tk.S)
    whiteBarDisplay.grid(row=1)
    ntDisplay.grid_propagate(0)


# class for window
class Win(tk.Tk):

    # window configuration and initiation
    def __init__(self):
        # basic window configurations
        super().__init__()
        self.item = None
        self.columnconfigure(0, weight=1)
        self.overrideredirect(True)
        self.grid_propagate(False)
        self.wm_geometry("1280x800")  # window size
        self.configure(background="#858585")  # window background color
        self.minsize(400, 400)  # minimum size for window

        # set starting position of window to be 0,0
        self.x = 0
        self.y = 0

        # -------------------------------------
        # create and configure custom title bar
        # -------------------------------------

        title_bar = tk.Frame(self, height=25, bg='#2e2e2e', relief='raised', bd=1)
        title_bar.grid(row=0, column=0, columnspan=5, sticky='ew')
        tk.Button(title_bar, text='x', command=self.destroy).pack(fill='x', side="right")

        # bind mouse button 1 to move window using title bar
        title_bar.bind('<ButtonPress-1>', self.button_press)
        title_bar.bind('<B1-Motion>', self.move_window)

        # -------------------------------------
        # create and configure frames for navigation bar, main console, timers
        # -------------------------------------
        sideBarFrame = tk.Frame(self, height=800, width=350, bg='#443E3E', relief='raised', bd=1)
        mainConsoleFrame = tk.Frame(self, height=700, width=1100, bg='#443E3E', relief='groove', bd=1)
        timerFrame = tk.Frame(self, height=100, width=1100, bg='#443E3E', relief='groove', bd=1)

        # configure grid layout  for each frame      
        sideBarFrame.grid(row=1, column=0, rowspan=4, sticky='w')
        mainConsoleFrame.grid(row=2, column=1, columnspan=4, sticky=tk.NW)
        timerFrame.grid(row=1, column=1, columnspan=4, sticky=tk.N)
        timerFrame.rowconfigure(0, weight=1)
        timerFrame.rowconfigure(1, weight=2)
        timerFrame.rowconfigure(2, weight=1)
        timerFrame.columnconfigure(0, weight=2)
        timerFrame.columnconfigure(1, weight=1)
        timerFrame.columnconfigure(2, weight=1)
        timerFrame.columnconfigure(3, weight=2)

        # disable resizing of frames to widgets
        mainConsoleFrame.grid_propagate(0)
        sideBarFrame.grid_propagate(0)
        timerFrame.grid_propagate(0)

        # create another frame within main console
        itemDisplayFrame = tk.Frame(mainConsoleFrame, width=250, height=150, bd=1, bg='#858585', relief='groove')
        itemDisplayFrame.grid(row=0, column=0, padx=10, pady=10)  # will need to configure in future to populate more
        # itemDisplayFrame.grid_propagate(0)  # disable resizing from widgets

        # -------------------------------------
        # Displays  * All display function calls will fall under here
        # -------------------------------------

        # -- displays for navigation bar
        navBarDisplay(sideBarFrame)
        # -- displays for Eorzea Time
        clockDisplay = EorzeanClock(timerFrame)
        clockDisplay.EorzeaTimeDisplay()
        # -- display for Local Time
        clockDisplay.LocalTimeDisplay()
        # call item node class
        ItemNode(itemDisplayFrame, 856, 34043)  # manually added numbers for testing

    # --------------------------------------
    # Functions
    # ---------------------------------------

    # function for moving window
    def move_window(self, event):
        x = self.winfo_pointerx() - self.x
        y = self.winfo_pointery() - self.y
        self.geometry('+{}+{}'.format(x, y))

    # function for button press
    def button_press(self, event):
        self.x = event.x
        self.y = event.y


win = Win()

win.mainloop()
