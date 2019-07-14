from django.http import HttpResponse, JsonResponse
import time
import uuid

class created:

    def __init__(self):
        self.time = lambda: int(round(time.time() * 1000))
        self.start = self.time()
        self.uuid = uuid.uuid4()

    def catch(self, request, data):
        self.meta = request.META['color']
        print(self.meta['LIGHT'] + "[RESPONSE CREATED - " + str(self.uuid) + "] " + request.build_absolute_uri('?') + '\n## BODY - ' + str(data) + ' :: ' + str(self.time() - self.start) + 'ms')
        res = JsonResponse(data, safe = False)
        res.status_code = 201
        return res
