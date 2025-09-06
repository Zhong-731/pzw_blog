from django.db import models

from user_app.models import User
from blog_app.models import Article

# Create your models here.
class ArticleComment(models.Model):
    '''
        文章评论模型
    '''
    comment = models.CharField(max_length=256, verbose_name='评论')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='文章')
    answer = models.ForeignKey(
                                'self', # 自关联
                                on_delete=models.CASCADE,
                                verbose_name='回答',
                                null=True,
                                blank=True,
                            )

    class Meta:
        db_table = 't_article_comment'

class Question(models.Model):
    '''
        问题反馈模型
    '''
    question = models.CharField(max_length=512,verbose_name='问题')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')

    class Meta:
        db_table = 't_question'
