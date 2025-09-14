from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AlreadyRegistered

User = get_user_model()

try:
    admin.site.register(User)
except AlreadyRegistered:
    # 如果已经注册则忽略，避免重复注册导致启动失败
    pass