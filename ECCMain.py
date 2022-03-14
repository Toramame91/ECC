import io
import json
import tkinter as tk
from datetime import datetime
from urllib.request import urlopen
import time
import requests
from PIL import ImageTk, Image


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
        title_bar.grid(row=0, column=0, columnspan=4, sticky='ew')
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
        mainConsoleFrame.grid(row=2, column=1, columnspan=3, sticky=tk.NW)
        timerFrame.grid(row=1, column=1, columnspan=3, sticky=tk.N)

        # disable resizing of frames to widgets
        mainConsoleFrame.grid_propagate(0)
        sideBarFrame.grid_propagate(0)
        timerFrame.grid_propagate(0)

        # create another frame within main console
        itemDisplayFrame = tk.Frame(mainConsoleFrame, width=250, height=150, bd=1, bg='#858585', relief='groove')
        itemDisplayFrame.grid(row=0, column=0, padx=10, pady=10)  # will need to configure in future to populate more
        # itemDisplayFrame.grid_propagate(0)  # disable resizing from widgets

        # -------------------------------------
        # API
        # -------------------------------------

        # API REQUESTS ************************

        # REQUESTS FOR GATHERING ITEM DATA
        gatheringInfo_API = requests.get('https://xivapi.com/GatheringPointBase/856?columns=Item1.Item')
        gatheringPointInfo_API = requests.get('https://xivapi.com/GatheringPoint/34043?columns=GatheringPointTransient,'
                                              'PlaceName,'
                                              'TerritoryType.PlaceName')

        # JSON CREATION ***********************

        # JSONS WITH GATHERING ITEM DATA
        gatheringPointBaseData = gatheringInfo_API.text
        parse_GatherPointBaseData = json.loads(gatheringPointBaseData)

        gatheringPointData = gatheringPointInfo_API.text
        parse_gatheringPointData = json.loads(gatheringPointData)

        # name parse, filters results and name from results.  Label displays results.
        itemName = parse_GatherPointBaseData['Item1']['Item']['Name']
        locationMapName = parse_gatheringPointData['TerritoryType']['PlaceName']['Name']
        locationPlaceName = parse_gatheringPointData['PlaceName']['Name']
        nodeSpawnTime0 = parse_gatheringPointData['GatheringPointTransient']['GatheringRarePopTimeTable']['StartTime0']
        nodeSpawnTime1 = parse_gatheringPointData['GatheringPointTransient']['GatheringRarePopTimeTable']['StartTime1']
        fNodeSpawnTime0 = f'{nodeSpawnTime0:04d}'
        fNodeSpawnTime1 = f'{nodeSpawnTime1:04d}'
        iconURLParse = parse_GatherPointBaseData['Item1']['Item']['IconHD']
        # IMAGE PARSE
        # open url to read into memory stream
        IconURL = urlopen(
            'https://static.wikia.nocookie.net/ffxiv_gamepedia/images/2/29/Elm_Lumber.png/revision/latest/scale-to-width-down/128?cb=20170114190928')
        # create image file object
        avatarPic = io.BytesIO(IconURL.read())
        # use PIL to open jpeg file then convert to image Tkinter can use
        pil_img = Image.open(avatarPic)
        resized = pil_img.resize((50, 50), Image.ANTIALIAS)
        itemImage = ImageTk.PhotoImage(resized)

        # LABEL
        tk.Label(itemDisplayFrame,
                 text="Name: " + itemName,
                 relief='flat', justify='left', bg='#858585').grid(row=0, column=1, columnspan=2)

        tk.Label(itemDisplayFrame,
                 text="Location: " + locationPlaceName + " ," + locationMapName,
                 relief='flat', justify='left', bg='#858585').grid(row=1, column=1, columnspan=2)

        iconDisplay = tk.Label(itemDisplayFrame, image=itemImage, bg="#202124")
        iconDisplay.grid(row=0, column=0, rowspan=2)
        iconDisplay.image = itemImage

        # labels for spawn time
        tk.Label(itemDisplayFrame,
                 text="Spawn Time", bg='#858585').grid(row=2, column=0, columnspan=2, sticky=tk.W)

        tk.Label(itemDisplayFrame,
                 text=fNodeSpawnTime0 + " / " + fNodeSpawnTime1, bg='#858585').grid(row=3, column=0,
                                                                                    columnspan=2, sticky=tk.W)

        # labels for active/cooldown timers
        tk.Label(itemDisplayFrame,
                 text="Active/ Cooldown", bg='#858585').grid(row=2, column=2, columnspan=2, sticky=tk.E)

        self.CooldownCountdown()

        # -------------------------------------
        # Displays  * All display function calls will fall under here
        # -------------------------------------

        # -- displays for navigation bar
        navBarDisplay(sideBarFrame)
        # -- displays for Eorzea Time
        self.EorzeaTimeDisplay()
        # -- display for Local Time
        self.LocalTimeDisplay()

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

    # Function for calculating Eorzea time and displaying on a label
    def EorzeaTimeDisplay(self):
        localEpoch = int(time.time() * 1000)  # local epoch time
        epoch = localEpoch * 20.57142857142857  # local epoch times 3600/175 for eorzea time conversion
        minutes = int((epoch / (1000 * 60)) % 60)  # ticks from epoch calculated into minutes
        hours = int((epoch / (1000 * 60 * 60)) % 24)  # ticks from epoch calculated into hours
        eHours = f'{hours:02d}'  # format hours to display 2 digits
        eMinutes = f'{minutes:02d}'  # format minutes to display 2 digits
        display = str(eHours) + ":" + str(eMinutes)  # combine hours and minutes into one string
        # label for time placement
        timerLbl = tk.Label(self, text="E.T.  " + display, bg='#443E3E', fg='white', font=('calibri', 20, 'bold'))
        timerLbl.grid(row=1, column=1)
        timerLbl.after(2550, self.EorzeaTimeDisplay)

    # Function for local time
    def LocalTimeDisplay(self):
        now = datetime.now()  # get current local time
        current_time = now.strftime("%H:%M:%S")  # display local time in Hour:Minute:Second format
        # label for time placement
        ctLabel = tk.Label(self, text="L.T.  " + current_time, bg='#443E3E', fg='white', font=('calibri', 20, 'bold'))
        ctLabel.grid(row=1, column=2)
        ctLabel.after(1000, self.LocalTimeDisplay)

    def CooldownCountdown(self):
        seconds = 2101

        while seconds > 0:
            minutes, secs = divmod(seconds, 60)
            timeFormat = '{:02d}:{:02d}'.format(minutes, secs)

            cdLabel = tk.Label(self,
                               text=timeFormat, bg='#858585')
            cdLabel.grid(row=0, column=0)
            seconds -= 1
            time.sleep(1)

            # cdLabel.after(1000, self.CooldownCountdown)

    def FindEorzeaTime(self):
        localEpoch = int(time.time() * 1000)  # local epoch time
        epoch = localEpoch * 20.57142857142857  # local epoch times 3600/175 for eorzea time conversion

        return epoch


win = Win()

win.mainloop()
