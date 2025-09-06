from django.contrib import admin
from django.db import models
from django.conf import settings

from tinymce.widgets import TinyMCE

from .models import Article, Tag, Category

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': TinyMCE(
                mce_attrs=settings.TINYMCE_DEFAULT_CONFIG,
                attrs={'cols': 80, 'rows': 30}  # 添加默认尺寸
            )
        },
    }
    
    # 添加列表显示配置
    list_display = ('title', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'content')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)