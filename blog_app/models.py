from django.db import models

from tinymce.models import HTMLField

from user_app.models import User

# Create your models here.
class Category(models.Model):
    category_choices = (
        (0,'学习'),
        (1,'生活'),
        (2,'其他'),
    )

    category = models.IntegerField(choices=category_choices,unique=True,verbose_name='分类名称')

    # def __str__(self):
    #     return f'{self.category}'

    class Meta:
        db_table = 't_category'

class Tag(models.Model):
    '''
        标签模型
    '''
    tag = models.CharField(max_length=10,verbose_name='标签名称')

    # def __str__(self):
    #     return self.tag

    class Meta:
        db_table = 't_tag'

class Article(models.Model):
    '''
        文章模型
    '''
    CHOICE_STATUS = (
        (0,'草稿'),
        (1,'发布'),
    )

    CHOICE_TYPE = (
        (0,'原创'),
        (1,'转载'),
    )


    title = models.CharField(max_length=100,verbose_name='文章标题')
    content = HTMLField(verbose_name=' 文章内容') # 富文本
    status = models.IntegerField(choices=CHOICE_STATUS,default=0,verbose_name='文章状态')
    type = models.IntegerField(choices=CHOICE_TYPE,default=0,verbose_name='文章类型')
    view_count = models.PositiveIntegerField(default=0,verbose_name='浏览次数')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐文章')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    category = models.ForeignKey(Category,
                                 related_name='articles',
                                 on_delete=models.CASCADE,
                                 verbose_name='文章分类'
                            )
    tags = models.ManyToManyField(Tag,
                                  related_name='articles',
                                  verbose_name='文章标签'
                            )
    user = models.ForeignKey(User,
                             related_name='acticles',
                             on_delete=models.CASCADE,
                             verbose_name='作者'
                        )

    class Meta:
        db_table = 't_article'
        ordering = ['-created_at'] # 倒序排序


# class TagArticle(models.Model):
#     '''
#         文章标签关系模型
#     '''
#     tag = models.ForeignKey(Tag,related_name='tag_articles',on_delete=models.CASCADE)
#     article = models.ForeignKey(Article,related_name='tag_articles',on_delete=models.CASCADE)

#     class Meta:
#         db_table = 't_tag_article'


# class ArticleAnswer(models.Model):
#     '''
#         文章评论模型
#     '''
#     article = models.ForeignKey(Article,related_name='comments',on_delete=models.CASCADE)
#     user = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
#     content = models.TextField()
#     create_at = models.DateTimeField(auto_now_add=True)


