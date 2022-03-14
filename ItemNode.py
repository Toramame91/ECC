import tkinter as tk
import json
import requests
import io
from PIL import ImageTk, Image

from urllib.request import urlopen


class ItemNode(object):

    def __init__(self, frame, itemID, gpID):
        self._frame = frame
        self._itemID = itemID
        self._GatheringPointID = gpID
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.SpawnTime0 = 0
        self.SpawnTime1 = 0

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
        nodeSpawnTime0 = parse_gatheringPointData['GatheringPointTransient']['GatheringRarePopTimeTable']['StartTime0']
        nodeSpawnTime1 = parse_gatheringPointData['GatheringPointTransient']['GatheringRarePopTimeTable']['StartTime1']
        fNodeSpawnTime0 = f'{nodeSpawnTime0:04d}'
        fNodeSpawnTime1 = f'{nodeSpawnTime1:04d}'
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
        tk.Label(self._frame,
                 text="Name: " + itemName,
                 relief='flat', justify='left', bg='#858585').grid(row=0, column=1, columnspan=2)

        tk.Label(self._frame,
                 text="Location: " + locationPlaceName + " ," + locationMapName,
                 relief='flat', justify='left', bg='#858585').grid(row=1, column=1, columnspan=2)

        iconDisplay = tk.Label(self._frame, image=itemImage, bg="#202124")
        iconDisplay.grid(row=0, column=0, rowspan=2)
        iconDisplay.image = itemImage

        # labels for spawn time
        tk.Label(self._frame,
                 text="Spawn Time", bg='#858585').grid(row=2, column=0, columnspan=2, sticky=tk.W)

        tk.Label(self._frame,
                 text=fNodeSpawnTime0 + " / " + fNodeSpawnTime1, bg='#858585').grid(row=3, column=0,
                                                                                    columnspan=2, sticky=tk.W)

        # labels for active/cooldown timers
        tk.Label(self._frame,
                 text="Active/ Cooldown", bg='#858585').grid(row=2, column=2, columnspan=2, sticky=tk.E)

    @property
    def getItemID(self):
        return self._itemID

    @property
    def getGatheringPointID(self):
        return self._GatheringPointID

    # def CooldownCountdown(self):
    #     seconds = 2101
    #
    #     while seconds > 0:
    #         minutes, secs = divmod(seconds, 60)
    #         timeFormat = '{:02d}:{:02d}'.format(minutes, secs)
    #
    #         cdLabel = tk.Label(self.frame,
    #                                text=timeFormat, bg='#858585')
    #         cdLabel.grid(row=0, column=0)
    #         seconds -= 1
    #         time.sleep(1)
