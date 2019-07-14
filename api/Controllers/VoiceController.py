from django.views.decorators.csrf import csrf_exempt
from django.views import View

from ..Modules.VoiceModule import VoiceData
from ..Policies.responseLog import response

res = response(None)

class Voice(View):
    
    @csrf_exempt
    def recordToData(request):
        data = VoiceData()
        response = data.upload(request)
        
        if 'error' in response:
            return res.badRequest(request, response)
        else:
            return res.ok(request, response)
