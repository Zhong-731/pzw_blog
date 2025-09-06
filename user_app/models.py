import hashlib

from django.db import models

# Create your models here.
class User(models.Model):
    '''
        用户模型
    '''
    username = models.CharField(max_length=15,unique=True,verbose_name='用户名')
    password = models.CharField(max_length=15,unique=True,verbose_name='用户密码')
    _password = models.CharField(null=True, blank=True,max_length=512, verbose_name='加密密码')
    nick_name = models.CharField(null=True,blank=True,max_length=15,verbose_name='用户昵称')
    phone = models.CharField(unique=True,max_length=11,verbose_name='电话号码')
    email = models.EmailField(unique=True,verbose_name='邮箱')
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