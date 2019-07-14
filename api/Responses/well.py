from django.http import HttpResponse, JsonResponse
import time
import uuid

class well:

    def __init__(self):
        self.time = lambda: int(round(time.time() * 1000))
        self.start = self.time()
        self.uuid = uuid.uuid4()

    def catch(self, request, data):
        self.meta = request.META['color']
        print(self.meta['GREEN'] + "[RESPONSE OK - " + str(self.uuid) + "] " + request.build_absolute_uri('?') + self.meta['LIGHT'] +  '\n## BODY - ' + str(data) + ' :: ' + str(self.time() - self.start) + 'ms')
        res = JsonResponse(data, safe = False)
        res.status_code = 200
        return res
