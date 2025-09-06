from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    '''
        注册功能序列化器
    '''
    # 细化字段规则
    username = serializers.CharField(required=True,min_length=3,max_length=15)
    password = serializers.CharField(required=True,min_length=6,max_length=15)
    nickname = serializers.CharField(required=False)
    phone = serializers.CharField(required=True)
    email = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def validate_username(self,uname):
        '''
            # 验证该用户名是否已经注册
        '''
        try:
            User.objects.get(username=uname)
            # 存在就要抛出
            raise serializers.ValidationError('该用户名已经被注册')
        except User.DoesNotExist:
            return uname


    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    '''
        用户列表序列化器
    '''

    class Meta:
        model = User
        fields = ['id', 'username', 'nick_name']


class UserDatailSerializer(serializers.ModelSerializer):
    '''
        用户详情序列化器
    '''

    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = '__all__'

