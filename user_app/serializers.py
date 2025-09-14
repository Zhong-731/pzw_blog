from rest_framework import serializers
from .models import User

from django.core.cache import cache


class PhoneRegisterSerializer(serializers.ModelSerializer):
    '''
        手机号注册视图序列化器
    '''
    # 细化字段规则
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True,min_length=6,max_length=20)
    sms_code = serializers.CharField(max_length=6, required=True)  # 用户提交的验证码

    def validate_phone(self, value):
        """
            # 验证该手机号是否已经注册
        """
        try:
            User.objects.get(phone=value)
            # 存在就要抛出
            raise serializers.ValidationError('该手机号已经被注册')
        except User.DoesNotExist:
            return value

    def validate_sms_code(self, value):
        """
            验证短信验证码是否正确
        """
        phone = self.initial_data.get("phone")
        cached_code = cache.get(f"sms_code_{phone}") # 
        if not cached_code or cached_code != value:
            raise serializers.ValidationError("验证码错误或已过期")
        return value

    def create(self, validated_data):
        """
            创建用户
        """
        phone = validated_data["phone"]
        password = validated_data["password"]
        user = User.objects.create(phone=phone, password=password)
        return user
    
    class Meta:
        model = User
        fields = '__all__'


class SocialAuthSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google', 'apple'])
    id_token = serializers.CharField()


class PhoneSendSerializer(serializers.Serializer):
    phone = serializers.CharField()


class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()
    name = serializers.CharField(required=False, allow_blank=True)


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', getattr(User, 'USERNAME_FIELD', 'username'), 'email')



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

