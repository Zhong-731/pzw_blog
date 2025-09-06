from django.db import models

from user_app.models import User

# Create your models here.
class Personal(models.Model):
    '''
        个人主页模型
    '''
    CHOICE_SEX = (
        (0,'男'),
        (1,'女'),
    )
    introduce = models.CharField(max_length=144,null=True,blank=True,verbose_name='个人简介')
    age = models.IntegerField(null=True,blank=True, verbose_name='年龄')
    sex = models.BooleanField(choices=CHOICE_SEX,default=0,verbose_name='性别')
    birthday = models.DateField(null=True,blank=True, verbose_name='生日')
    address = models.CharField(null=True,blank=True,max_length=10, verbose_name='地址')

    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='用户')

    class Meta:
        db_table = 't_personal'
