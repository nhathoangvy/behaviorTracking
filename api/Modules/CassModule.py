from cassandra.cluster import Cluster

class cass:
    def __init__(self):
        self.cluster = Cluster(['localhost:3000'])
        self.session = self.cluster.connect('userexperience')

    def query(self, cql):
        cql = cql + 'ALLOW FILTERING;'
        rows = self.session.execute(cql)
        return rows
