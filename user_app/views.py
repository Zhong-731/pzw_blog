from django.core.cache import cache
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView 
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as grequests

from user_app.models import User
from user_app.token import generate_token,verify_token
from .serializers import PhoneRegisterSerializer, UserListSerializer, UserDatailSerializer 

import random

# Create your views here.
class SendSMSView(APIView):
    """
    发送短信验证码——（手机号注册、登录）
    """
    def post(self, request):
        phone = request.data.get("phone")

        if not phone:
            return Response({"code": 400, "msg": "手机号或密码不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        # 生成6位随机验证码
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        
        # # 调用阿里云短信接口
        # client = AcsClient(settings.ALIYUN_SMS["ACCESS_KEY_ID"], settings.ALIYUN_SMS["ACCESS_KEY_SECRET"], "default")
        # sms_request = SendSmsRequest.SendSmsRequest()
        # sms_request.set_SignName(settings.ALIYUN_SMS["SIGN_NAME"])
        # sms_request.set_TemplateCode(settings.ALIYUN_SMS["TEMPLATE_CODE"])
        # sms_request.set_PhoneNumbers(phone)
        # sms_request.set_TemplateParam("{\"code\":\"" + code + "\"}")  # 模板变量
 
        try:
            # response = client.do_action_with_exception(sms_request)
            # 存储验证码到缓存（5分钟有效期）
            cache.set(f"sms_code_{phone}", code, 300)  # key格式：sms_code_<手机号>
            return Response({
                "code": 200,
                "msg": "短信发送成功",
                "sms_code": code
                })
        except Exception as e:
            return Response({"code": 500, "msg": f"短信发送失败: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PhoneRegisterView(APIView):
    '''
        手机号注册视图（带短信验证码验证）
    '''
    def post(self,request):
        # 反序列化
        serializer = PhoneRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 注册成功后删除缓存的验证码（防止重复使用）
            phone = serializer.validated_data["phone"]
            cache.delete(f"sms_code_{phone}")
            return Response({
                "code": status.HTTP_201_CREATED,
                'msg': '用户注册成功'
            })
        else:
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                'msg': serializer.errors
            })


class PhoneLoginView(APIView):
    '''
        手机号登录视图
    '''
    def post(self, request):
        # 接收参数
        phone = request.data.get('phone')
        password = request.data.get('password')
        sms_code = request.data.get('sms_code')
        # 非空判断
        if sms_code != cache.get(f"sms_code_{phone}"):
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "msg": "验证码错误"
            })
        
        # 非空判断
        if not phone or not password:
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "msg": "手机号和密码不能为空"
            })

         # 验证参数
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({
                "code": status.HTTP_404_NOT_FOUND,
                "msg": "用户不存在" 
            })
             
        if user.check_password(password):
            token = generate_token({'phone': user.phone})
            return Response({
                "code": status.HTTP_200_OK,
                "msg": "登录成功！",
                "token": token  
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'msg': '密码错误'
            })

class GoogleLoginView(APIView):
    '''
        Google 登录视图
    '''
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = request.data.get('id_token')
        if not id_token:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'msg': 'id_token为空'
            })

        try:
            # 验证 id_token（会验证签名、过期等）
            id_info = google_id_token.verify_oauth2_token(
                id_token, grequests.Request(), settings.GOOGLE_CLIENT_ID
            )
        except Exception as e:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'msg': 'id_token无效',
                'error': str(e)
                })

        # 可额外校验 issuer / aud 等
        if id_info.get('aud') != settings.GOOGLE_CLIENT_ID:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'msg': 'audience 无效'
                })

        email = id_info.get('email')
        sub = id_info.get('sub')  # Google 用户唯一 id
        name = id_info.get('name')
        picture = id_info.get('picture')

        # 使用 email 查找用户（根据项目需要调整）
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': email.split('@')[0] or sub}
        )

        if created:
            # 不设置可登录密码，除非你想允许密码登录
            user.set_unusable_password()
            user.save()
            # 如果有用户 profile 存 social id，可写入 sub 等信息

        # 生成 JWT（access + refresh）
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'name': name,
                'picture': picture
            }
        })
    


class PasswordChangeView(APIView):
    def put(self, request):
        '''
            密码修改功能 (token)
        '''
        data = verify_token(request.META.get('HTTP_AUTHORIZATION'))
        if data:
            try:
                user = User.objects.get(phone = data.get('phone'))
            except Exception as e:
                return Response ({
                    'code' : status.HTTP_400_BAD_REQUEST,
                    'msg' : '用户信息有误'
                })

            # 接收修改密码的参数
            old_password = request.data.get('old_password')
            
            # 验证参数
            if user.check_password(old_password):
                new_password1 = request.data.get('new_password1')
                new_password2 = request.data.get('new_password2')
                if (new_password1 == new_password2) and new_password1 :
                    user.password = new_password1
                    user.save()
                    return Response({
                        'code' : status.HTTP_200_OK,
                        'msg' : '修改密码成功，请重新登录！',
                        'redirect' : 'user/login/'
                    })
                else:
                    return Response({
                        'code' : status.HTTP_400_BAD_REQUEST,
                        'msg' : '两次新密码不相同'
                    })
            else:
                return Response({
                    'code' : status.HTTP_400_BAD_REQUEST,
                    'msg' : '原密码不正确'
                })
        else:
            return Response({
                "code" : status.HTTP_401_UNAUTHORIZED,
                "msg" : '请先登录',
                'redirect' : 'user/login/'
            })


class UserListView(ListAPIView):
    '''
        获取用户列表
    '''
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    '''
        获取用户详情
    '''
    queryset = User.objects.all()
    serializer_class = UserDatailSerializer


