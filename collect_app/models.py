from django.db import models

from user_app.models import User
from blog_app.models import Article

# Create your models here.
class CollectArticle(models.Model):
    '''
        文章收藏模型
    '''
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='收藏时间')

    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='文章')
    

    class Meta:
        db_table = 't_collect_Article'
        unique_together = (('user', 'article'),) # 联合约束 确保同一个用户不能重复收藏同一篇文章
        verbose_name = '收藏'
    

