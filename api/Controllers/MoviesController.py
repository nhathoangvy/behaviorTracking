from django.views.decorators.csrf import csrf_exempt
from django.views import View

from ..Modules.RelatedModule import Related
from ..Policies.responseLog import response

res = response(None)

class Movies(View):
    
    @csrf_exempt
    def get(request):
        data = Related()
        response = data.content(request)
        
        if 'error' in response:
            return res.badRequest(request, response)
        else:
            return res.ok(request, response)
