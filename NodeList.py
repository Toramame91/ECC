import requests
import ItemNode
import time


class NodeLists:
    def __init__(self):
        self._ewDictLegendary = {856: 34043, 858: 34045}

    def GetEndwalkerDict(self):
        return self._ewDictLegendary.get()

    def EndwalkerDictItems(self):
        return self._ewDictLegendary.items()

    def EndwalkerDictCount(self):
        return len(self._ewDictLegendary)
