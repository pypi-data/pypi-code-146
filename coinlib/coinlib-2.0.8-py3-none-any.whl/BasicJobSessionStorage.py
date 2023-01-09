import datetime
import json
import time

import numpy as np

from coinlib import Registrar


class LastSignalValue:
    found: bool
    value: any
    distanceTicks: int
    distanceSeconds: int
    time: str
    date: datetime.datetime
    ticks: int

class BasicJobSessionStorage():

    def __init__(self, storageData=None):
        self._changed = False
        self._lastStorage = {}
        self.registrar = Registrar()
        self._storage = {}
        if storageData is None:
            storageData = {}
        self._storage = storageData
        self._lastStorage = {}
        self._lastIndex = self.findLastIndex()
        self._currentIndex = self._lastIndex
        self._currentTicks = 0
        self.updateLastValuesOfStorage()
        pass

    def resetLastValue(self):
        self._lastStorage = {}

    ## needs to be tested - is not final
    def updateLastValuesOfStorage(self):
        indexes = [x for x in self._storage.keys()]
        indexes.sort(key=lambda x: time.strptime(x, "%Y-%m-%d-%H:%M:%S"))
        indexes.reverse()
        ticks = 0
        maxRounds = 300
        for k_index in indexes:
            if k_index in self._storage:
                for key in self._storage[k_index]:
                    value = self._storage[k_index][key]
                    try:
                        if value is not None and not np.isnan(value):
                            last = LastSignalValue()
                            last.value = self._storage[k_index][key]
                            last.distanceTicks = ticks
                            lastTime = datetime.datetime.strptime(k_index, "%Y-%m-%d-%H:%M:%S")
                            last.time = lastTime
                            last.ticks = ticks
                            currentTime = datetime.datetime.strptime(self._lastIndex, "%Y-%m-%d-%H:%M:%S")
                            last.distanceSeconds = (currentTime - lastTime).total_seconds()
                            last.found = True
                            if key not in self._lastStorage:
                                self._lastStorage[key] = last
                                self.registrar.logger.info("Last Storage set: "+key+": "+json.dumps(last))

                    except Exception as e:
                        pass

            ticks = ticks + 1
            if ticks > maxRounds:
                break

    def getSignalData(self):
        return list(self._lastStorage.keys())

    def saveInfo(self, group, key, value):
        self.setData(group+"."+key, value)

    def setCurrentIndex(self, index, moveLastValues=False):
        if index is not None:
            index = index.strftime("%Y-%m-%d-%H:%M:%S")
            if self._currentIndex == index:
                return
            """ if moveLastValues:
                self._changed = False
                if self._lastIndex in self._storage:
                    self._storage[index] = {}
                    for key in self._storage[self._lastIndex]:
                        if "var." in key:
                            self._storage[index][key] = self._storage[self._lastIndex][key]
                else:
                    self._storage[index] = {}"""
            self._lastIndex = self._currentIndex
            self._currentIndex = index
            self._currentTicks = self._currentTicks + 1


    def findLastIndex(self):
        maxdate = None
        if len(self._storage.keys()) > 0:
            maxdate = max((x for x in self._storage.keys()), key=lambda x: time.strptime(x, "%Y-%m-%d-%H:%M:%S"))
        return maxdate

    def hasChanged(self):
        return self._changed

    def clear(self):
        self._changed = False
        self.storage = {}

    def unset(self, key, index=None):
        if index is None:
            index = self._currentIndex
        if index in self._storage:
            if key in self._storage[index]:
                self._changed = True
                del self._storage[index][key]
                return True

        return False


    def delete(self, key, index=None):
        if index is None:
            index = self._currentIndex
        return self.unset(index, key)

    def getData(self, key, defaultValue = None, index=None):
        if index is None:
            e = self.getData(key, defaultValue=defaultValue, index=self._currentIndex)
            if e is not None:
                return e
            index = self._lastIndex
        if index not in self._storage:
            return defaultValue
        if key not in self._storage[index]:
            return defaultValue

        return self._storage[index][key]


    def getLastData(self, key, maxSecondsDistance=None) -> LastSignalValue:
        last = LastSignalValue()
        last.found = False
        last.value = None
        if key in self._lastStorage:
            nv = self._lastStorage[key]
            lastTime = datetime.datetime.strptime(nv.time, "%Y-%m-%d-%H:%M:%S") if isinstance(nv.time, str) else nv.time
            currentTime = datetime.datetime.strptime(self._lastIndex, "%Y-%m-%d-%H:%M:%S")
            ticks = self._currentTicks - nv.ticks if self._currentTicks > 0 else nv.ticks
            distance = (currentTime - lastTime).total_seconds()
            if maxSecondsDistance is not None:
                if distance > maxSecondsDistance:
                    return last

            last.time = nv.time
            last.date = lastTime
            last.found = True
            last.value = nv.value
            last.distanceSeconds = distance
            last.distanceTicks = ticks


        return last

    def _setLastData(self, key, value):
        last = LastSignalValue()
        last.time = self._currentIndex
        last.ticks = self._currentTicks
        last.value = value

        self._lastStorage[key] = last
        return last

    def setData(self, key, value, index= None):
        if index is None:
            index = self._currentIndex
        if index not in self._storage:
            self._storage[index] = {}
            self._changed = True
        if key not in self._storage[index]: #  or self._storage[index][key] != value # need this check later on
            self._changed = True
        self._storage[index][key] = value
        self._setLastData(key, value)

        return value

    def resetChanges(self):
        self._changed = False

    def getStorage(self):
        return self._storage

    def getStorageIndexed(self):
        storage = {}
        index = 0
        for key in self._storage.keys():
            storage[index] = self._storage[key]
            index = index + 1
        return storage

    def getCurrentStorageRow(self):
        if self._currentIndex is not None:
            if self._currentIndex in self._storage:
                return self._storage[self._currentIndex]
        return {}

    def getLastStorageRow(self):
        if self._lastIndex is not None:
            if self._lastIndex in self._storage:
                return self._storage[self._lastIndex]
        return {}

    def setVar(self, logicId, name, data):
        return self.setData(logicId+".var."+name, data)

    def getVar(self, logicId, name):
        d = self.getLastData(logicId+".var."+name)
        if d is None:
            return None
        if d.found:
            if isinstance(d.value, list):
                return None
            return d.value
        return None

    def setSignal(self, logicId, name, data):
        return self.setData(logicId+".signal."+name, data)

    def getLastSignal(self, logicId, name, maxSecondsDistance =None) -> LastSignalValue:
        lsignal = self.getLastData(logicId+".signal."+name, maxSecondsDistance=maxSecondsDistance)

        return lsignal

    def getSignal(self, logicId, name):
        return self.getData(logicId+".signal."+name)
