from rest_framework import serializers
from .models import CollectArticle

class CollectArticleListSerializer(serializers.ModelSerializer):
    '''
        文章收藏列表序列化器
    '''
    article_title = serializers.CharField(source='article.title') 
    author = serializers.CharField(source='article.user.nick_name')
    category = serializers.CharField(source='article.category.category')
    tags = serializers.StringRelatedField(source='article.tags.tag') # 多对多
    article_created_at = serializers.DateTimeField(source='article.created_at',format='%Y-%m-%d %H:%M:%S')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = CollectArticle
        fields = ['article_title', 'author', 'category', 'tags', 'article_created_at', 'created_at']
        ordering = ['-created_at']