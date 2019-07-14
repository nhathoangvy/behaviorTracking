from ..Responses.badRequest import badRequest
from ..Responses.well import well
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseForbidden

class response(Exception):

    def __init__(self, get_response):
        self.logs = logs()

    def ok (self, request, data):
        return self.logs.ok(request, data)

    def badRequest(self, request, data):
        return self.logs.badRequest(request, data)

class logs(object):
    def __init__(self):
        pass

    def ok(self, request, data):
        ok = well()
        return ok.catch(request, data)

    def badRequest(self, request, data):
        badReq = badRequest()
        return badReq.catch(request, data)