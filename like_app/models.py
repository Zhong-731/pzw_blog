from django.db import models
from django.utils import timezone

from user_app.models import User
from blog_app.models import Article
from question_app.models import ArticleComment

# Create your models here.
class LikeArticle(models.Model):
    '''
        文章点赞模型
        
    '''
    created_at = models.DateTimeField(default=timezone.now, verbose_name='点赞时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='点赞用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='文章')

    class Meta:

        db_table = 't_like_article'
        unique_together = ('user', 'article')


class LikeComment(models.Model):
    '''
        评论点赞模型
    '''
    created_at = models.DateTimeField(default=timezone.now, verbose_name='点赞时间')

    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='点赞用户')
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, verbose_name='评论')

    class Meta:

        db_table = 't_like_comment'
        unique_together = ('user', 'comment')