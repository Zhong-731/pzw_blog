import hashlib

from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    '''
        用户模型（支持手机号登录和注册）
    '''
    username = models.CharField(null=True, blank=True, max_length=15,unique=True,verbose_name='用户名')
    password = models.CharField(null=True, blank=True, max_length=15,unique=True,verbose_name='用户密码')
    _password = models.CharField(null=True, blank=True,max_length=512, verbose_name='加密密码')
    nick_name = models.CharField(null=True,blank=True,max_length=15,verbose_name='用户昵称')
    phone = models.CharField(unique=True,max_length=11,verbose_name='电话号码') # 不能为空
    email = models.EmailField(null=True,blank=True, unique=True,verbose_name='邮箱')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='用户创建时间')

    # def __str__(self):
    #     return self.username  

    class Meta:
        db_table = 't_user'

    
    @property # 加了property 方法变成了属性，每次密码时调用就会执行，返回加密密码
    def password(self):
        return self._password
    
    @password.setter # 这个装饰器允许password赋值,每次password修改时，_password也会被修改
    def password(self, pwd):
        self._password = hashlib.md5(pwd.encode('utf-8')).hexdigest()

    def check_password(self, raw_pwd):
        '''
            验证密码
            :parmas raw_pwd 原生密码 
        '''
        pwd = hashlib.md5(raw_pwd.encode('utf-8')).hexdigest()
        return pwd == self._password
    
class SocialAccount(models.Model):
    """
        将第三方登录的 provider（google/apple）和 provider uid 与本地用户关联
    """
    PROVIDER_CHOICES = [
        ('google', 'Google'),
        ('apple', 'Apple'),
    ]

    uid = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES)

    class Meta:
        unique_together = ('provider', 'uid')


class PhoneOTP(models.Model):
    """
        存储手机号发送的验证码与状态（便于审计 / 防刷 / 重复发送控制）
    """
    phone = models.CharField(max_length=32, db_index=True)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    def mark_verified(self):
        self.verified = True
        self.save(update_fields=['verified'])