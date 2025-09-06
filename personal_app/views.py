from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from user_app.token import TokenPermission
from user_app.models import User
from .models import Personal
from .serializers import PersonalDetailSerializer




# Create your views here.
class PersonalAddView(APIView):
    permission_classes = (TokenPermission,)
    
    def post(self, request):
        '''
            添加个人主页信息
        '''
        try:
            # 检查用户是否存在
            personal = Personal.objects.get(user__phone=request.user)

            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'msg': '个人主页已存在'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Personal.DoesNotExist:
            # 创建个人主页
            serializer = PersonalDetailSerializer(data=request.data)
            if serializer.is_valid():
                from user_app.models import User
                user = User.objects.get(phone=request.user)
                serializer.save(user=user)
                return Response({
                    'code': status.HTTP_201_CREATED,
                    'msg': '个人主页信息创建成功',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'msg': '数据验证失败',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

    



class PersonalUpdateView(APIView):
    permission_classes = (TokenPermission,)
    
    def put(self, request):
        '''
            更新个人主页信息
        '''
        if request.data.get('nick_name'):
            user = User.objects.get(phone=request.user)
            user.nick_name = request.data.get('nick_name')
            user.save()

        try:
            personal = Personal.objects.get(user__phone=request.user)
            serializer = PersonalDetailSerializer(personal, data=request.data, partial=True)
            


            if serializer.is_valid():
                serializer.save()

                return Response({
                    'code': status.HTTP_200_OK,
                    'msg': '更新成功',
                    'data': serializer.data
                })
            else:
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'msg': '数据验证失败',
                    'errors': serializer.errors
                })
                
        except Personal.DoesNotExist:
            return Response({
                'code': status.HTTP_404_NOT_FOUND,
                'msg': '个人主页不存在'
            }, status=status.HTTP_404_NOT_FOUND)


class PersonalDetailView(APIView):
    '''
        获取个人主页信息
    '''
    permission_classes = (TokenPermission,)
    
    def get(self, request):
        '''
            获取个人主页信息
        '''
        try:
            personal = Personal.objects.get(user__phone=request.user)
            serializer = PersonalDetailSerializer(personal)
            return Response({
                'code': status.HTTP_200_OK,
                'msg': '获取成功',
                'data': serializer.data
            })
        except Personal.DoesNotExist:
            return Response({
                'code': status.HTTP_404_NOT_FOUND,
                'msg': '个人主页信息不存在'
            }, status=status.HTTP_404_NOT_FOUND)

