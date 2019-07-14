import time
import math
import json
import sys
sys.path.append(".")
from behavior.api.Modules.RedisModule import redis
from behavior.tracking.sql import db

cacheBackup = db()
re = redis()
expireTime = 60*60*24*30
limited = 31

class logic:
    def __init__(self):
        self.color = {
            'GRAY' : '\033[37m',
            'ORANGE' : '\033[1;31m',
            'RED' : '\033[31m',
            'GREEN' : '\033[1;32m',
            'YELLOW' : '\033[1;33m',
            'BLUE' : '\033[1;34m',
            'PURPLE' : '\033[1;35m',
            'LIGHT' : '\033[1;36m'
        }
        self.data = {
            'users' : [],
            'scores' : []
        }

    def mapping(self, stringData):
        stringData = stringData.decode()
        stringData = stringData.split('click:')
        userId = stringData[0]
        movieId = stringData[1]
        timing = str(math.ceil(time.time()/(60*60)))
        items = []
        try:
            stages = re.list('Tracking:'+userId+'-at-*')
        except MultiValueDictKeyError:
            stages = None
        if stages is not None:
            length = len(stages)
        else:
            length = 0
        if length != 0:
            numk = 0
            for k in stages:
                k = k.decode()
                k = k.split('-at-')
                timeStage = eval(k[1])
                if timeStage > numk:
                    numk = timeStage

            timeStageLastest = str(numk)
            stageLastest = re.get('Tracking:'+userId+'-at-'+timeStageLastest)
            dataStage = eval(stageLastest.decode())

            if movieId not in dataStage:
                dataStage.append(movieId)

            if float(timeStageLastest) < float(timing):
                re.setup('Tracking:'+userId+'-at-'+timing,json.dumps([movieId]),expireTime)
                print(self.color['GREEN'] + 'NEW TRACKED ' +userId+'-at-'+timing)
            else:
                re.setup('Tracking:'+userId+'-at-'+ timeStageLastest,json.dumps(dataStage),expireTime)
                print(self.color['GREEN'] + 'TRACKED ' +userId+'-at-'+timeStageLastest)
        else:
            items.append(movieId)
            re.setup('Tracking:'+userId+'-at-'+timing,json.dumps(items),expireTime)
            print(self.color['GREEN'] + 'TRACKED NEW KEY '+userId+'-at-'+timing)

        if length > 3:
            historyDataStages = []
            firstItem = []
            secondItem = []
            thirdItem = []

            for sk in stages:
                sk = sk.decode()
                data = eval(re.get(sk).decode())
                historyDataStages.append(data)

            for dataStage in historyDataStages:
                for data in dataStage:
                    if data not in firstItem:
                        firstItem.append(data)
                    elif data not in secondItem:
                        secondItem.append(data)
                    else:
                        if len(thirdItem) < 31:
                            thirdItem.append(data)

            if len(thirdItem) < 31:
                for item in secondItem:
                    if item not in thirdItem and len(thirdItem) < 31:
                        thirdItem.append(item)
                    else:
                        for itemChild in firstItem:
                            thirdItem.append(itemChild)

            stored = self.matrix(thirdItem)
            re.setup('recommemdation:'+userId,json.dumps(stored),expireTime)

            cacheBackup.query(
                """INSERT INTO Mapping VALUES ("%s","%s","%s")
                ON DUPLICATE KEY UPDATE content = "%s", hoursTiming = "%s" """% (
                userId, stored, timing, stored, timing
            ))
            print(self.color['GREEN'] + 'MATRIX TRACKING '+ userId)
            for kdone in stages:
                kdone = kdone.decode()
                re.delete(kdone)
        return

    def matrix(self, data):

        firstItem = []
        secondItem = []
        thirdItem = []

        for item in data:
            itemData = re.get('related:' + item)
            itemData = eval(itemData.decode())
            for itemItemData in itemData:
                if itemItemData not in firstItem:
                    firstItem.append(itemItemData)
                elif itemItemData not in secondItem:
                    secondItem.append(itemItemData)
                else:
                    if len(thirdItem) < 31:
                        thirdItem.append(itemItemData)

        if len(thirdItem) < 31:
            for item in secondItem:
                if item not in thirdItem and len(thirdItem) < 31:
                    thirdItem.append(item)
                else:
                    if len(thirdItem) < 31:
                        for itemChild in firstItem:
                            thirdItem.append(itemChild)

        return thirdItem
