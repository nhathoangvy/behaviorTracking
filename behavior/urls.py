
from django.contrib import admin
from django.urls import path
from django.conf.urls import *

from api.Controllers import *

admin.autodiscover()

urlpatterns = [
    path('/health_check', CheckController.health.check, name = 'get'),
    path('/recommemdation/auth', AuthController.Auth.login, name = 'login'),
    path('/related/movie', MoviesController.Movies.get, name = 'get'),
    path('/voice/data', VoiceController.Voice.recordToData, name = 'upload')
]
