from django.contrib import admin

from .models import ArticleComment, Question
# Register your models here.
admin.site.register(ArticleComment)
admin.site.register(Question)