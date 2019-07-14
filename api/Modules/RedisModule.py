import redis
r = redis.Redis(
    host='10.10.11.196',
    port=6379,
    password='')

class redis:
    def __init__(self):
        self.client = r
        # self.client = redis.Redis(
        #     host='localhost',
        #     port=6379,
        #     db=0,
        #     password=None,
        #     socket_timeout=None,
        #     socket_connect_timeout=None,
        #     socket_keepalive=None,
        #     socket_keepalive_options=None,
        #     connection_pool=None,
        #     unix_socket_path=None,
        #     encoding='utf-8',
        #     encoding_errors='strict',
        #     charset=None, errors=None,
        #     decode_responses=False,
        #     retry_on_timeout=False,
        #     ssl=False,
        #     ssl_keyfile=None,
        #     ssl_certfile=None,
        #     ssl_cert_reqs=None,
        #     ssl_ca_certs=None,
        #     max_connections=None
        # )

    def get(self, key):
        data = self.client.get(key)
        if data:
            return data
        else:
            return None

    def list(self, arg):
        data = self.client.keys(arg)
        if data:
            return data
        else:
            return None

    def setup(self,key,val,time):
        if time:
            self.client.setex(key,val,time)
        else:
            self.client.set(key,val)
        return

    def delete(self, key):
        self.client.delete(key)
        return
