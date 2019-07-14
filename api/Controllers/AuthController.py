from django.views.decorators.csrf import csrf_exempt
from django.views import View

from ..Modules.AuthModule import AuthModule
from ..Policies.responseLog import response

res = response(None)

class Auth(View):
    
    @csrf_exempt
    def login(request):
        data = AuthModule()
        response = data.login(request)
        
        if 'error' in response:
            return res.badRequest(request, response)
        else:
            return res.ok(request, response)
