import math
import time
from .CassModule import cass
selfcass = cass()
class logic:
    def __init__(self):
        self.data = {
            'movieId' : '',
            'users' : [],
            'scores' : []
        }

    def explore(self, movieId):
        cql = """
            SELECT * FROM movie WHERE id = '%s'
        """% (movieId)
        rows = selfcass.query(cql)
        self.data['movieId'] = movieId
        for row in rows:
            if row.length > 0:
                point = math.ceil((row.progress/row.length) * 100)
                self.data['scores'].append(point)
            self.data['users'].append(row.profile_id)
        self.data['timestamp'] = math.ceil(time.time())
        return self.data
