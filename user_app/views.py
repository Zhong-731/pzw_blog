from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView 

from user_app.models import User
from user_app.token import generate_token,verify_token
from .serializers import RegisterSerializer, UserListSerializer, UserDatailSerializer 

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        '''
            注册功能
        '''
        # 反序列化
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # 保存
            serializer.save()
            return Response({
                "code" : status.HTTP_201_CREATED,
                'msg' : '用户注册成功'
            })
        else:
            return Response({
                "code" : status.HTTP_400_BAD_REQUEST,
                'msg' : serializer.errors
            })


class LoginView(APIView):
    def post(self,request):
        '''
            登录功能
        '''
        # 接收参数
        username = request.data.get('username')

         # 验证参数
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return Response({
                "code" : status.HTTP_404_NOT_FOUND,
                "msg" : "用户不存在" 
            })
        
        try:
            password = request.data.get('password')
        except Exception as e:
            return Response({
                "code" : status.HTTP_404_NOT_FOUND,
                "msg" : "密码不能为空" 
            })
        
        if user.check_password(password):
            token = generate_token({'phone': user.phone})
            return Response({
                "code" : status.HTTP_200_OK,
                "msg" : "登录成功！",
                "token" : token  
            })
        else:
            return Response({
                'code' : status.HTTP_400_BAD_REQUEST,
                'msg' : '密码错误'
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


