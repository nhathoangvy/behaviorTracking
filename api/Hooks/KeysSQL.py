from django.db import connection
import MySQLdb

class Keys:
    def __init__(self):
        self.result = []
        self.single = None

    def query(self, sqlQuery ,squelize):
        if squelize:
            sql = MySQLdb.connect(host=squelize['host'],
                        user=squelize[user], 
                        passwd=squelize[password], 
                        db=squelize[db],
                        port=squelize[port])   
        else:
            sql = connection
        values = sql.cursor()
        values.execute(sqlQuery)
        keys = values.description
        values = values.fetchall()
        for val in values:
            item = {}
            count = 0
            for key in keys:
                item[key[0]] = val[count]
                count += 1
            self.result.append(item)

        if (len(self.result) < 2 and len(self.result) > 0):
            self.single = self.result[0]
            return self.single
        if (len(self.result) == 0):
            return None
        else:
            return self.result
