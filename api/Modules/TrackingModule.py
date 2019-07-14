import json
from datetime import datetime
from .MQModule import MQ
# import sys
# sys.path.append("...")
from .LogicModule import logic
from ..Hooks.KeysSQL import Keys

REC_CHANNEL = 'REC'
RELATED_CHANNEL = 'REL'

class Tracking:

    def __init__(self):
        self.logic = logic()

    def send(self,movieId,userId):
        message = MQ()
        if userId and movieId:
            message.send(userId+'click:'+movieId,REC_CHANNEL)
            message.sendRel(json.dumps(self.logic.explore(movieId)),RELATED_CHANNEL)
        return

    def history(self,start,end):
        K = Keys()
        timeStart = datetime(datetime.strptime(start, '%Y-%m-%d %H:%M:%S'))
        timeEnd = datetime(datetime.strptime(end, '%Y-%m-%d %H:%M:%S'))
        if (timeEnd - timeStart).days > 1:
            self.result['error'] = 'Just get for each days'
        else:
            self.data = {
                "report": {
                    "host": "localhost",
                    "user": "report",
                    "password": "",
                    "db": "rp_db",
                    "port": 3306
                },
                "user" : 
                    """
                        select * from User
                        where adddate(createdAt , interval 7 hour) BETWEEN "%s" and "%s"
                    """% (start, end),
                "session" : 
                    """
                        select * from token where adddate(tk.createdAt , interval 7 hour) BETWEEN "%s" and "%s"
                    """% (start, end),
                "transaction" : 
                    """
                        select * from transaction
                        where adddate(t.createdAt , interval 7 hour) BETWEEN "%s" and "%s"
                    """% (start, end, start, end)
            }
            self.result = {
                "user" : K.query(self.data['user'], self.data['report']),
                "session" : K.query(self.data['session'], self.data['report']),
                "transaction" :  K.query(self.data['transaction'], self.data['report'])
            }
        return self.result