from .TrackingModule import Tracking
from .RedisModule import redis
from django.utils.datastructures import MultiValueDictKeyError
import re
from ..Hooks.KeysSQL import Keys
import random

class Related:
    def __init__(self):
        self.result = {}
        self.cache = redis()
        self.tracking = Tracking()

    def content(self, request):
        req = request.GET
        K = Keys()
        try:
            movieId = req['movieId']
        except KeyError as name:
            movieId = None

        try:
            userId = request.META['userId']
        except KeyError as name:
            userId = None
        if userId:
            self.tracking.send(movieId,userId)
        else:
            self.tracking.send(movieId,None)
        if movieId:
            data = self.cache.get(
                'related:' + movieId
            )
            self.result['related'] = []
            if data is None:
                dataCache = self.cache.list('related:*')
                dataItem = random.choice(dataCache)
                dataKey = dataItem.decode()
                data = self.cache.get(dataKey)

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
                self.result['related'] = rec
                #Tracking.log(movieId, access_token)
            else:
                sqlQuery = """
                    SELECT * FROM movie
                    WHERE id = '%s' AND status = 1
                """% (data[0])
                item = K.query(sqlQuery, False)
                self.result['related'].append(item)
        else:
            self.result['error'] = 'Missing params'

        return self.result
