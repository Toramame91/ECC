import tkinter as tk
import tkinter.ttk as ttk
from turtle import right
import requests
import json
from item import *
import asyncio
import pyxivapi
from pyxivapi.models import Filter, Sort

#class for window
class Win(tk.Tk):

    #window configuation and initiation
    def __init__(self):
        #basic window configurations
        super().__init__()
        self.columnconfigure(0, weight=1)        
        self.overrideredirect(True)
        self.grid_propagate(False)
        self.wm_geometry("1280x800")   #window size
        self.configure(background="#858585") #window background color
        self.minsize(400, 400) #minimum size for window

        #set starting position of window to be 0,0
        self.x = 0  
        self.y = 0

        # -------------------------------------
        # create and configure custom title bar
        # -------------------------------------
        
        title_bar = tk.Frame(self, height=25, bg='#2e2e2e', relief='raised', bd=1)
        title_bar.grid(row=0, column=0,columnspan=2, sticky='ew')
        tk.Button(title_bar, text='x', command=self.destroy).pack(fill='x', side="right")
             
        #bind mouse button 1 to move window using title bar
        title_bar.bind('<ButtonPress-1>', self.button_press)
        title_bar.bind('<B1-Motion>', self.move_window)

        # -------------------------------------
        # create and configure frames for navigation bar, main console, timers
        # -------------------------------------
        sideBarFrame = tk.Frame(self, height=800,width= 350, bg='#443E3E', relief='raised', bd=1)   
        mainConsoleFrame = tk.Frame(self, height=600,width= 1100, bg='#443E3E', relief='groove', bd=1)
        timerFrame = tk.Frame(self,height=200,width= 1100, bg='#443E3E', relief='groove', bd=1)

        #configure grid layout  for each frame      
        sideBarFrame.grid(row=1,column=0,rowspan=4, sticky='w') 
        mainConsoleFrame.grid(row=2,column=1,sticky=tk.NW)
        timerFrame.grid(row=1,column=1,sticky=tk.N)

        #disable resizing of frames to widgets
        mainConsoleFrame.grid_propagate(0)
        sideBarFrame.grid_propagate(0)

        #create another frame within main console
        itemDisplayFrame = tk.Frame(mainConsoleFrame,width=150,height=150,bd=1,bg='#858585')
        itemDisplayFrame.grid(row=0,column=0,padx=20,pady=20)  # will need to configure in future to populate more than 1
        itemDisplayFrame.grid_propagate(0)  #disable resizing from widgets    
        
        # -------------------------------------
        # API
        # -------------------------------------

        #request API
        response_API = requests.get('https://xivapi.com/item/36195?columns=ID,Name,Icon,Description,LevelItem')

        #create JSON to load from
        data = response_API.text
        parse_json = json.loads(data)

        #name parse, filters results and name from results.  Label displays results.
        itemName = parse_json['Name']
        itemID = parse_json['ID']
        inDisplay = tk.Label(itemDisplayFrame, text= "Name: "+itemName+"\n"+"item ID: "+str(itemID), relief='flat',justify='left',bg='#858585' ).grid(row=1,column=1,sticky=tk.W)

        # -------------------------------------
        # Displays  * All display function calls will fall under here
        # -------------------------------------
        
        ### displays for navigation bar
        self.navBarDisplay(sideBarFrame)
        

    #function for moving window
    def move_window(self, event):
        x = self.winfo_pointerx() - self.x
        y = self.winfo_pointery() - self.y
        self.geometry('+{}+{}'.format(x, y))

    #function for button press
    def button_press(self, event):
        self.x = event.x
        self.y = event.y

    def itemDisplayFrame(self,item):        
        tooltipFrame = tk.Frame(self.itemGrid)
        self.item = item        
        itemDLabel = tk.Label(self, text = "".format(item.id))
        itemDLabel.pack()

    def navBarDisplay(self,Frame):
        #create title bar for navigation menu
        frame = Frame

        whitebarDisplay = tk.Label(frame,text="__________________________________",bg='#443E3E', fg='white')
        ntDisplay = tk.Label(frame, text="Quick Access", bg='#443E3E', fg='white')
        ntDisplay.grid(row=0,column=0,sticky=tk.S)        
        whitebarDisplay.grid(row=1)
        ntDisplay.grid_propagate(0)

    

win = Win()


win.mainloop()


