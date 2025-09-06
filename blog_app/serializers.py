from rest_framework import serializers
from .models import Article

class ArticleDetailSerializer(serializers.ModelSerializer):
    '''
        文章详情序列化器
    '''
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Article
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    '''
        个人文章列表序列化器
    '''

    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Article
        exclude  = ['content']
        ordering = ['-created_at']


class ArticleAllListSerializer(serializers.ModelSerializer):
    '''
        所有文章列表序列化器
    '''
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Article
        exclude = ['content']
        ordering = ['-created_at']  
        