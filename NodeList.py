class NodeLists:
    def __init__(self):
        self._ewNodeListLegendary = [34043, 34044, 34045, 33967, 33968, 33969]
        self._ewNodeListEphemeral = [34047, 34048, 34050, 34052]

    def GetEndwalkerListLegendary(self):
        return self._ewNodeListLegendary

    def EndwalkerListLegendaryCount(self):
        return len(self._ewNodeListLegendary)

    def GetEndwalkerListEphemeral(self):
        return self._ewNodeListEphemeral

    def EndwalkerListEphemeralCount(self):
        return len(self._ewNodeListEphemeral)
