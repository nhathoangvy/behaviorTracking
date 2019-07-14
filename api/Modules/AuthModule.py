from django.utils.datastructures import MultiValueDictKeyError
# import sys
# sys.path.append("...")
# import os, json
# from classification.predict import Predict
import requests
from .RedisModule import redis
from .RecommemdationModule import Rec
import json
PRODUCT_CAS = "http://localhost:8080"
CAS_LOGIN = PRODUCT_CAS + "/login"
CAS_INFO = PRODUCT_CAS + "/info"

class AuthModule:
    def __init__ (self):
        self.cache = redis()
        self.req = requests
        self.headers = {
            'content-type': 'application/json',
            "api-key" : "sercet"
        }
        self.data = {}
        self.rec = Rec()
        self.result = {}

    def login(self, request):
        if request.method == "POST":
            req = request.POST
            try:
                userId = request.META['userId']
            except KeyError as name:
                userId = None
            try:
                self.data['mobile'] = req['mobile']
                self.data['password'] = req['password']
            except MultiValueDictKeyError:
                self.data['mobile'] = False
                self.data['password'] = False

            if self.data['mobile'] != False and self.data['password'] != False :
                self.data['services'] = ["auth"]
                ticket = self.req.post(
                    CAS_LOGIN,
                    headers=self.headers,
                    data=json.dumps(self.data)
                )
                try:
                    self.result['token'] = ticket.json()['tickets'][0]['ticket']
                except KeyError as name:
                    self.result['token'] = None

                if self.result['token'] is None:
                    self.result['error'] = 'Login again'
                else:
                    userInfo = self.req.post(
                        CAS_INFO,
                        headers=self.headers,
                        data = json.dumps({
                            "ticket": self.result['token']
                        })
                    )
                    userId = userInfo.json()['userInfo']['id']
                    self.cache.setup(
                        'cache:'+self.result['token'],
                        userId,
                    60*60*24)
                    self.result['recommemdation'] = self.rec.hook(userId)
                    self.result['trend'] = []
            elif userId:
                self.result['recommemdation'] = self.rec.hook(userId)
                self.result['trend'] = []
            else:
                self.result['error'] = 'Login again'

        else:
            self.result['error'] = 'Something wrong'

        return self.result
