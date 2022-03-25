import tkinter as tk
import json
import requests
import io
import requests_cache

from PIL import ImageTk, Image
from Clocks import *
from urllib.request import urlopen, Request


class ItemNode(object):

    def __init__(self, frame, gpID, nodeNum):
        self._frame = frame
        self._nodeFrame = None
        self._GatheringPointID = gpID
        self.nodeNumber = nodeNum
        self._realWorldSeconds = 0
        self._labelFont = ('helvetica', 10)
        self.SpawnTime0 = 0
        self.SpawnTime1 = 0
        self.activeTimer = 160
        self.active = False
        self.cdLabel = None
        self.SpawnLabelText = tk.StringVar()
        self.API_URL = "https://xivapi.com"

        # create another frame within main console
        itemDisplayFrame = tk.Frame(self._frame, width=250, height=160, bd=1, bg='#858585', relief='groove')
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
        gatherDataCache = requests.get(
            f'https://xivapi.com/GatheringPoint/{self._GatheringPointID}?private_key=45484ebc973f443fae7a525fc0557ac832dacf8e079c47e195717cf0f6df32dd')

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
        iconURLParse0 = self.API_URL + parse_gatheringPointData['GatheringPointBase']['Item0']['Item']['Icon']
        iconURLParse1 = self.API_URL + parse_gatheringPointData['GatheringPointBase']['Item1']['Item']['Icon']
        iconURLParseGtype = self.API_URL + parse_gatheringPointData['GatheringPointBase']['GatheringType']['IconMain']
        req0 = Request(iconURLParse0, headers={'User-Agent': 'Mozilla/5.0'})
        req1 = Request(iconURLParse1, headers={'User-Agent': 'Mozilla/5.0'})
        reqGType = Request(iconURLParseGtype, headers={'User-Agent': 'Mozilla/5.0'})
        # IMAGE PARSE
        # open url to read into memory stream
        iconURL0 = urlopen(req0)
        iconURL1 = urlopen(req1)
        iconURLGType = urlopen(reqGType)

        # create image file object
        itemIcon0read = io.BytesIO(iconURL0.read())
        itemIcon1read = io.BytesIO(iconURL1.read())
        itemGatheringTypeRead = io.BytesIO(iconURLGType.read())
        # use PIL to open jpeg file then convert to image Tkinter can use
        pil_img0 = Image.open(itemIcon0read)
        pil_img1 = Image.open(itemIcon1read)
        pil_imgGType = Image.open(itemGatheringTypeRead)

        resizedIcon0 = pil_img0.resize((25, 25), Image.ANTIALIAS)
        resizedIcon1 = pil_img1.resize((25, 25), Image.ANTIALIAS)
        resizedIconGType = pil_imgGType.resize((25, 25), Image.ANTIALIAS)

        itemIcon0 = ImageTk.PhotoImage(resizedIcon0)
        itemIcon1 = ImageTk.PhotoImage(resizedIcon1)
        gatheringTypeIcon = ImageTk.PhotoImage(resizedIconGType)

        # LABEL
        tk.Label(itemDisplayFrame,
                 text=itemName0,
                 relief='flat', justify='left', bg='#858585', font=self._labelFont).grid(row=0, column=1, sticky=tk.W)

        tk.Label(itemDisplayFrame,
                 text=itemName1,
                 relief='flat', justify='left', bg='#858585', font=self._labelFont).grid(row=1, column=1, sticky=tk.W)

        tk.Label(itemDisplayFrame,
                 text=locationPlaceName + " ," + locationMapName,
                 relief='flat', justify='left', bg='#858585', font=self._labelFont).grid(row=2, column=0, columnspan=4,
                                                                                         sticky=tk.W)

        # Icon Displays
        iconDisplay0 = tk.Label(itemDisplayFrame, image=itemIcon0, bg="#858585")
        iconDisplay0.grid(row=0, column=0, sticky=tk.W)
        iconDisplay0.image = itemIcon0

        iconDisplay1 = tk.Label(itemDisplayFrame, image=itemIcon1, bg="#858585")
        iconDisplay1.grid(row=1, column=0, sticky=tk.W)
        iconDisplay1.image = itemIcon1

        gatheringIconDisplay = tk.Label(itemDisplayFrame, image=gatheringTypeIcon, bg="#858585")
        gatheringIconDisplay.grid(row=5, column=0, sticky=tk.W)
        gatheringIconDisplay.image = gatheringTypeIcon

        # labels for spawn currentTime
        tk.Label(itemDisplayFrame,
                 text=fNodeSpawnTime0 + " / " + fNodeSpawnTime1 + " Eorzean Time", bg='#858585',
                 font=self._labelFont).grid(
            row=3, column=0,
            columnspan=2,
            sticky=tk.W)

        # labels for active/cooldown timers

        currentEorzeaTime = EorzeanClock.ConvertEorzea(self)
        self._realWorldSeconds = self.FindRealSeconds(self.FindNextSpawn(currentEorzeaTime))
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
        if self.SpawnTime0 < currentTime < (self.SpawnTime0 + 160):
            self.active = True
            self._realWorldSeconds = self.FindRealSeconds(
                self.FindRemainingActiveTime(EorzeanClock.ConvertEorzea(self)))
        elif self.SpawnTime1 < currentTime < (self.SpawnTime1 + 160):
            self.active = True
            self._realWorldSeconds = self.FindRealSeconds(
                self.FindRemainingActiveTime(EorzeanClock.ConvertEorzea(self)))
        else:
            self.active = False

    def FindNextSpawn(self, currentTime):
        spawn0 = self.SpawnTime0 - 40
        spawn1 = self.SpawnTime1 - 40
        if self.SpawnTime0 < currentTime < self.SpawnTime1:
            result = abs(spawn1 - currentTime)
        elif 2400 > currentTime > self.SpawnTime1:
            result = abs(2360 - currentTime)
            result = spawn0 + result
        elif currentTime < self.SpawnTime0:
            result = abs(spawn0 - currentTime)

        return result

    def FindRemainingActiveTime(self, currentTime):
        if self.SpawnTime0 <= currentTime < (self.SpawnTime0 + 160):
            result = abs((self.SpawnTime0 + 160) - currentTime)
        elif self.SpawnTime1 <= currentTime < (self.SpawnTime1 + 160):
            result = abs((self.SpawnTime1 + 160) - currentTime)
        return result

    def CooldownCountdown(self):
        minutes, secs = divmod(self._realWorldSeconds, 60)
        timeFormat = '{:02d}:{:02d}'.format(minutes, secs)
        self.SpawnLabelText.set("Spawns In: " + timeFormat)
        self.cdLabel = tk.Label(self._nodeFrame, textvariable=self.SpawnLabelText, bg='#858585', fg='red',
                                justify='left',
                                font=self._labelFont)
        self.cdLabel.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        self._realWorldSeconds -= 1
        if self._realWorldSeconds < 1:
            self.active = True
            time.sleep(1)
            self._realWorldSeconds = 350
            self.ActiveCountdown()
        else:

            self.cdLabel.after(1000, self.CooldownCountdown)

    def ActiveCountdown(self):
        minutes, secs = divmod(self._realWorldSeconds, 60)
        timeFormat = '{:02d}:{:02d}'.format(minutes, secs)
        self.SpawnLabelText.set("Spawn Active: " + timeFormat)
        self.cdLabel = tk.Label(self._nodeFrame, textvariable=self.SpawnLabelText, bg='#858585', fg='green',
                                justify='left',
                                font=self._labelFont)
        self.cdLabel.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        self._realWorldSeconds -= 1
        if self._realWorldSeconds < 1:
            self.active = False
            time.sleep(1)
            self._realWorldSeconds = 1750
            self.CooldownCountdown()
        else:
            self.cdLabel.after(1000, self.ActiveCountdown)
