import tkinter as tk
import json
import requests
import io

from PIL import ImageTk, Image
from Clocks import *
from urllib.request import urlopen


class ItemNode(object):

    def __init__(self, frame, itemID, gpID, nodeNum):
        self._frame = frame
        self._nodeFrame = None
        self._itemID = itemID
        self._GatheringPointID = gpID
        self.nodeNumber = nodeNum
        self.sec = 0
        self.SpawnTime0 = 0
        self.SpawnTime1 = 0
        self.activeTimer = 2
        self.active = False

        # create another frame within main console
        itemDisplayFrame = tk.Frame(self._frame, width=250, height=150, bd=1, bg='#858585', relief='groove')
        xGrid = int(self.nodeNumber / 4)
        if self.nodeNumber > 3:
            self.nodeNumber = int(self.nodeNumber % 4)
        itemDisplayFrame.grid(row=xGrid, column=self.nodeNumber, padx=10, pady=10)  # will need to configure in future to populate more
        self._nodeFrame = itemDisplayFrame
        # itemDisplayFrame.grid_propagate(0)  # disable resizing from widgets

        # -------------------------------------
        # API
        # -------------------------------------

        # API REQUESTS ************************

        # REQUESTS FOR GATHERING ITEM DATA
        gatheringInfo_API = requests.get(f'https://xivapi.com/GatheringPointBase/{self._itemID}?columns=Item1.Item')
        gatheringPointInfo_API = requests.get(
            f'https://xivapi.com/GatheringPoint/{self._GatheringPointID}?columns=GatheringPointTransient,PlaceName,TerritoryType.PlaceName')

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
        self.SpawnTime0 = int(parse_gatheringPointData['GatheringPointTransient']['GatheringRarePopTimeTable']['StartTime0'])
        self.SpawnTime1 = int(parse_gatheringPointData['GatheringPointTransient']['GatheringRarePopTimeTable']['StartTime1'])
        fNodeSpawnTime0 = f'{self.SpawnTime0:04d}'
        fNodeSpawnTime1 = f'{self.SpawnTime1:04d}'
        iconURLParse = parse_GatherPointBaseData['Item1']['Item']['IconHD']
        # IMAGE PARSE
        # open url to read into memory stream
        IconURL = urlopen(
            'https://static.wikia.nocookie.net/ffxiv_gamepedia/images/2/29/Elm_Lumber.png/revision/latest/scale-to'
            '-width-down/128?cb=20170114190928')
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

        currentEorzeaTime = EorzeanClock.ConvertEorzea(self)
        self.sec = int(self.FindNextSpawn(currentEorzeaTime) / 100) * 175

        if self.active is False:
            self.CooldownCountdown()
        elif self.active is True:
            self.ActiveCountdown()

    @property
    def getItemID(self):
        return self._itemID

    @property
    def getGatheringPointID(self):
        return self._GatheringPointID

    def FindNextSpawn(self, currentTime):
        if self.SpawnTime0 < currentTime < self.SpawnTime1:
            result = abs(self.SpawnTime1 - currentTime)
        elif currentTime > self.SpawnTime1:
            result = abs(2400 - currentTime)
            result = abs(self.SpawnTime0 + result)
        elif currentTime < self.SpawnTime0:
            result = abs(self.SpawnTime0 - currentTime)

        return result

    def CooldownCountdown(self):
        minutes, secs = divmod(self.sec, 60)
        timeFormat = '{:02d}:{:02d}'.format(minutes, secs)
        cdLabel = tk.Label(self._nodeFrame, text=timeFormat, bg='#858585', fg='red')
        cdLabel.grid(row=3, column=2)
        self.sec -= 1
        if self.sec <= -1:
            self.active = True
            self.sec = self.activeTimer * 175
            self.ActiveCountdown()

        cdLabel.after(1000, self.CooldownCountdown)

    def ActiveCountdown(self):
        minutes, secs = divmod(self.sec, 60)
        timeFormat = '{:02d}:{:02d}'.format(minutes, secs)
        actLabel = tk.Label(self._nodeFrame, text=timeFormat, bg='#858585', fg='green')
        actLabel.grid(row=3, column=2)
        self.sec -= 1
        if self.sec <= -1:
            self.active = False
            self.sec = int(self.FindNextSpawn(EorzeanClock.ConvertEorzea(self)) / 100) * 175
            self.CooldownCountdown()

        actLabel.after(1000, self.ActiveCountdown)




