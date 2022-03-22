import tkinter as tk
import json
import requests
import io
import requests_cache

from PIL import ImageTk, Image
from Clocks import *
from urllib.request import urlopen


class ItemNode(object):

    def __init__(self, frame, gpID, nodeNum):
        self._frame = frame
        self._nodeFrame = None
        self._GatheringPointID = gpID
        self.nodeNumber = nodeNum
        self.sec = 0
        self.font = ('helvetica', 10)
        self.SpawnTime0 = 0
        self.SpawnTime1 = 0
        self.activeTimer = 160
        self.active = False

        # create another frame within main console
        itemDisplayFrame = tk.Frame(self._frame, width=250, height=175, bd=1, bg='#858585', relief='groove')
        xGrid = int(self.nodeNumber / 4)
        if self.nodeNumber > 3:
            self.nodeNumber = int(self.nodeNumber % 4)
        itemDisplayFrame.grid(row=xGrid, column=self.nodeNumber, padx=10, pady=10)
        self._nodeFrame = itemDisplayFrame
        itemDisplayFrame.grid_propagate(0)  # disable resizing from widgets

        # -------------------------------------
        # API
        # -------------------------------------

        # API REQUESTS ************************

        # REQUESTS FOR GATHERING ITEM DATA
        requests_cache.install_cache('testCache', backend='sqLite')
        gatherDataCache = requests.get(f'https://xivapi.com/GatheringPoint/{self._GatheringPointID}')

        # JSON CREATION ***********************

        # JSONS WITH GATHERING ITEM DATA

        gatheringPointData = gatherDataCache.text
        parse_gatheringPointData = json.loads(gatheringPointData)

        # name parse, filters results and name from results.  Label displays results.
        itemName0 = parse_gatheringPointData['GatheringPointBase']['Item0']['Item']['Name']
        itemName1 = parse_gatheringPointData['GatheringPointBase']['Item1']['Item']['Name']
        locationMapName = parse_gatheringPointData['TerritoryType']['PlaceName']['Name']
        locationPlaceName = parse_gatheringPointData['PlaceName']['Name']
        self.SpawnTime0 = int(
            parse_gatheringPointData['GatheringPointTransient']['GatheringRarePopTimeTable']['StartTime0'])
        self.SpawnTime1 = int(
            parse_gatheringPointData['GatheringPointTransient']['GatheringRarePopTimeTable']['StartTime1'])
        fNodeSpawnTime0 = f'{self.SpawnTime0:04d}'
        fNodeSpawnTime1 = f'{self.SpawnTime1:04d}'
        # iconURLParse = parse_GatherPointBaseData['Item1']['Item']['IconHD']
        # IMAGE PARSE
        # open url to read into memory stream
        IconURL = urlopen(
            'https://static.wikia.nocookie.net/ffxiv_gamepedia/images/2/29/Elm_Lumber.png/revision/latest/scale-to'
            '-width-down/128?cb=20170114190928')
        # create image file object
        avatarPic = io.BytesIO(IconURL.read())
        # use PIL to open jpeg file then convert to image Tkinter can use
        pil_img = Image.open(avatarPic)
        resized = pil_img.resize((25, 25), Image.ANTIALIAS)
        itemImage = ImageTk.PhotoImage(resized)

        # LABEL
        tk.Label(itemDisplayFrame,
                 text=itemName0,
                 relief='flat', justify='left', bg='#858585', font=self.font).grid(row=0, column=1, sticky=tk.W)

        tk.Label(itemDisplayFrame,
                 text=itemName1,
                 relief='flat', justify='left', bg='#858585', font=self.font).grid(row=1, column=1, sticky=tk.W)

        tk.Label(itemDisplayFrame,
                 text=locationPlaceName + " ," + locationMapName,
                 relief='flat', justify='left', bg='#858585', font=self.font).grid(row=2, column=0, columnspan=4,
                                                                                   sticky=tk.W)

        iconDisplay1 = tk.Label(itemDisplayFrame, image=itemImage, bg="#858585")
        iconDisplay1.grid(row=0, column=0, sticky=tk.W)
        iconDisplay1.image = itemImage

        iconDisplay2 = tk.Label(itemDisplayFrame, image=itemImage, bg="#858585")
        iconDisplay2.grid(row=1, column=0, sticky=tk.W)
        iconDisplay2.image = itemImage

        # labels for spawn currentTime
        tk.Label(itemDisplayFrame,
                 text=fNodeSpawnTime0 + " / " + fNodeSpawnTime1 + " Eorzean Time", bg='#858585', font=self.font).grid(
            row=3, column=0,
            columnspan=2,
            sticky=tk.W)

        # labels for active/cooldown timers

        currentEorzeaTime = EorzeanClock.ConvertEorzea(self)
        self.sec = self.FindRealSeconds(self.FindNextSpawn(currentEorzeaTime))
        self.IsActive(currentEorzeaTime)
        if not self.active:
            self.CooldownCountdown()
        elif self.active:
            self.ActiveCountdown()

    @property
    def getGatheringPointID(self):
        return self._GatheringPointID

    def FindRealSeconds(self, currentTime):
        hours, minutes = divmod(currentTime, 100)
        convertHours = hours * 175
        convertSeconds = minutes * (2 + (11 / 12))
        realSeconds = int(convertHours) + int(convertSeconds)
        return realSeconds

    def IsActive(self, currentTime):
        if self.SpawnTime0 < currentTime < (self.SpawnTime0 + 200):
            self.active = True
            self.sec = self.FindRealSeconds(((self.SpawnTime0 + 160) - currentTime))
        elif self.SpawnTime1 < currentTime < (self.SpawnTime1 + 200):
            self.active = True
            self.sec = self.FindRealSeconds(((self.SpawnTime1 + 160) - currentTime))
        else:
            self.active = False

    def FindNextSpawn(self, currentTime):
        spawn0 = self.SpawnTime0 - 40
        spawn1 = self.SpawnTime1 - 40
        if self.SpawnTime0 < currentTime < self.SpawnTime1:
            result = abs(spawn1 - currentTime)
        elif 2400 > currentTime > self.SpawnTime1:
            result = abs(2400 - currentTime)
            result = spawn0 + result
        elif currentTime < self.SpawnTime0:
            result = abs(spawn0 - currentTime)

        return result

    def FindNextSpawnT(self, currentTime):
        nextTime = None
        if currentTime > self.SpawnTime0:
            nextTime = self.SpawnTime1
        if currentTime > self.SpawnTime1:
            nextTime = self.SpawnTime0
        if nextTime == 0:
            nextTime = 2400
        result = nextTime - currentTime
        print(result)
        return result

    def CooldownCountdown(self):
        minutes, secs = divmod(self.sec, 60)
        timeFormat = '{:02d}:{:02d}'.format(minutes, secs)
        cdLabel = tk.Label(self._nodeFrame, text="spawns in: " + timeFormat, bg='#858585', fg='red', justify='left',
                           font=self.font)
        cdLabel.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        self.sec -= 1
        if self.sec < 1:
            self.active = True
            self.sec = 350
            self.ActiveCountdown()

        cdLabel.after(1000, self.CooldownCountdown)

    def ActiveCountdown(self):
        minutes, secs = divmod(self.sec, 60)
        timeFormat = '{:02d}:{:02d}'.format(minutes, secs)
        actLabel = tk.Label(self._nodeFrame, text="active: " + timeFormat, bg='#858585', fg='green', justify='left',
                            font=self.font)
        actLabel.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        self.sec -= 1
        if self.sec < 1:
            self.active = False
            self.sec = 1750
            self.CooldownCountdown()

        actLabel.after(1000, self.ActiveCountdown)
