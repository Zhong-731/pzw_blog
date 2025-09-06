from rest_framework import serializers

from .models import Personal

class PersonalDetailSerializer(serializers.ModelSerializer):
    '''
        个人主页详情序列化器
    '''
    nick_name = serializers.CharField(source = 'user.nick_name', read_only=True)

    class Meta:
        model = Personal
        fields = ('id','nick_name','age','sex','birthday','address','introduce')