from django.contrib import admin
# 导入ArticlePost
from .models import ArticlePost, ArticleColumn

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)

admin.site.register(ArticleColumn)