from rest_framework import serializers

from question_app.models import ArticleComment,Question

class ArticleCommentDetailSerializer(serializers.ModelSerializer):
    '''
        个人文章评论详情序列化器
    '''
    
    nick_name = serializers.CharField(source = 'user.nick_name')
    article_title = serializers.CharField(source = 'article.title')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = ArticleComment
        fields = ['comment','created_at','nick_name','article_title','answer']

class ArticleCommentListSerializer(serializers.ModelSerializer):
    '''
        个人文章评论列表序列化器
    '''

    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = ArticleComment
        exclude = ['answer']


class QuestionDetailSerializer(serializers.ModelField):
    '''
        意见反馈详情序列化器
    '''
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Question
        fields = '__all__'


class QuestionListSerializer(serializers.ModelField):
    '''
        意见反馈列表序列化器
    '''
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Question
        fields = '__all__'