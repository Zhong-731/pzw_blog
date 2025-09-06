from rest_framework import serializers

from .models import LikeArticle,LikeComment

class LikeArticleListSerializer(serializers.ModelSerializer):
    '''
        点赞文章列表序列化器
    '''
    
    article_title = serializers.CharField(source='article.title')
    article_created_at = serializers.DateTimeField(source='article.created_at', format='%Y-%m-%d %H:%M:%S')
    like_created_at  = serializers.DateTimeField(source='created_at', format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = LikeArticle
        fields = ['article_title','article_created_at','like_created_at']