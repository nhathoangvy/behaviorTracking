import random
import json
from .RedisModule import redis
from ..Hooks.KeysSQL import Keys

class Rec:
    def __init__ (self):
        self.cache = redis()
        self.result = []
        #tcp = MQ()

    def hook(self, userId):
        K = Keys()
        data = self.cache.get(
            'recommemdation:' + userId
        )
        if data is None:
            dataCache = self.cache.list('recommemdation:*')
            dataItem = random.choice(dataCache)
            dataKey = dataItem.decode()
            data = self.cache.get(dataKey)
            #tcp.send(userId, REC_CHANNEL)

        data = eval(data.decode())
        if len(data) > 0:
            itemArray = []
            for i in range(0,12):
                itemId = random.choice(data)
                if itemId not in itemArray:
                    itemArray.append(itemId)
            itemArray = '", "'.join((str(n) for n in itemArray))
            sqlQuery = """
                SELECT * FROM movie
                WHERE id in ("%s") AND status = 1
            """% (itemArray)
            rec = K.query(sqlQuery, False)
            self.result = rec
        else:
            sqlQuery = """
                SELECT * FROM movie AND status = 1
                WHERE id = '%s' AND status = 1
            """% (data[0])
            item = K.query(sqlQuery, False)
            self.result.append(item)
        return self.result
