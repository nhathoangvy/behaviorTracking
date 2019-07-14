from django.views.decorators.csrf import csrf_exempt
from django.views import View

from ..Modules.TrackingModule import Tracking
from ..Policies.responseLog import response

res = response(None)

class History(View):
    
    @csrf_exempt
    def list(request):
        data = Tracking()
        response = data.history(request)
        
        if 'error' in response:
            return res.badRequest(request, response)
        else:
            return res.ok(request, response)
