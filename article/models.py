from django.db import models
# 导入User模型
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.

class ArticleColumn(models.Model):
    """
    文章栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)

    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# 博客文章数据类型
class ArticlePost(models.Model):
    # 文章作者， on_delete 用于指定数据删除方式
    # ForeignKey 用来表示"一对多"的关系，一篇文章由一个作者编写，而一个作者可以编写多篇文章
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    # 文章标签
    tags = TaggableManager(blank=True)

    # 文章标题（CharField为字符串字段）
    title = models.CharField(max_length=100)

    # 文章正文（保存大量文本使用TextFiled）
    body = models.TextField()

    # 浏览量
    total_views = models.PositiveIntegerField(default=0)

    # 文章创建时间（default=timezone.now表示在其创建数据时默认写入当前时间）
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间（auto_now=True 指每次更新数据时自动写入当前时间）
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据排列顺序
        # ‘-created’ 表明倒序排列
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    def __str__(self):
        return self.title
