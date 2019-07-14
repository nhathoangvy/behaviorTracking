from django.utils.datastructures import MultiValueDictKeyError
import re
import os
from ..Models.Files import Upload
import speech_recognition as sr

class VoiceData:
    def __init__(self):
        self.result = {}
        self.r = sr.Recognizer()

    def upload(self, request):
        if request.method == 'POST':
            try:
                try: 
                    lang = request.META['HTTP_LANGUAGE']
                    if lang is None:
                        lang = 'vi'
                except KeyError:
                    lang = 'vi'
                data = self.export(request.FILES['voice'], lang)
                self.result['data'] = data
            except MultiValueDictKeyError:
                self.result['error'] = 'Something wrong, try again'

        else:
            self.result['error'] = 'Use method POST'

        return self.result
    
    def export(self,soundByte,language):
        try:
            sounds = sr.AudioFile(soundByte)
            with sounds as source:
                self.r.adjust_for_ambient_noise(source) #duration=0.5
                audio = self.r.record(source) # offset=2, duration=4
            try:
                data = self.r.recognize_google(audio,language=language)
            except MultiValueDictKeyError:
                print("ERROR")
                data = None
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
                data = None
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                data = None
                
        except ValueError:
            data = None
        return data