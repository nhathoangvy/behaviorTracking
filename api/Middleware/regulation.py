import re
import json

from ..Modules.RedisModule import redis

class rules:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cache = redis()
        self.color = {
            'GRAY' : '\033[37m',
            'ORANGE' : '\033[1;31m',
            'RED' : '\033[31m',
            'GREEN' : '\033[1;32m',
            'YELLOW' : '\033[1;33m',
            'BLUE' : '\033[1;34m',
            'PURPLE' : '\033[1;35m',
            'LIGHT' : '\033[1;36m'
        }

    def __call__(self, request):
        try:
            access_token = request.META['HTTP_AUTHORIZATION'] if re.match("^[a-zA-Z0-9-]*$", request.META['HTTP_AUTHORIZATION']) else request.META['HTTP_AUTHORIZATION'] if len(request.META['HTTP_AUTHORIZATION']) > 50 else None

        except KeyError as name:
            access_token = None

        try:
            userData = request.META['HTTP_USER'] if json.loads(request.META['HTTP_USER']) else None
        except KeyError as name:
            userData = None

        if access_token:
            userId = self.cache.get('cache:'+ access_token)
            if userId:
                request.META['userId'] = userId.decode()
            else:
                request.META['userId'] = userData['userInfo']['id'] if userData else None
        else:
            try:
                request.META['userId'] = request.GET['uuid'] if re.match("^[a-zA-Z0-9-]*$", request.GET['uuid']) else userData['userInfo']['currentUUID'] if userData else None

            except KeyError as name:
                request.META['userId'] = None

        request.META['color'] = self.color
        return self.get_response(request)
