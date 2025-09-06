from rest_framework import status

from django.http import JsonResponse

from .token import verify_token

class LoginRequireMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/v1/user/'):
            if not verify_token(request.META.get("HTTP_AUTHORIZATion")):
                return JsonResponse({
                    'code' : status.HTTP_401_UNAUTHORIZED,
                    'msg' : '请先登录'
                }, json_dumps_params={'ensure_ascii' : False})
            
        
        return self.get_response(request)