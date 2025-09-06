'''
    JWT 工具类 ： 验证用户登录状态
'''
import time

import jwt 
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed

from user_app.models import User

from django.conf import settings

def generate_token(data:dict):
    '''
        生成token
    '''
    data.update({'exp' : settings.JWT_EXPIRE + time.time()})

    token = jwt.encode(data, settings.JWT_SECRET_KEY, algorithm='HS256')
    return token


def verify_token(token):
    '''
        解析token
    '''
    try: # 过期处理
        data = jwt.decode(token,settings.JWT_SECRET_KEY, algorithms=['HS256'])
    except Exception as e:
        return None

    return data


class TokenPermission(BasePermission):
    def has_permission(self, request, view):
        '''
            token权限认证
        '''
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            request.user = data.get('phone')
            return True
        else:
            raise AuthenticationFailed('请先登录')      
      
        
