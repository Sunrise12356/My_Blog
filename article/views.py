# 引入redirect重定向模块
from django.shortcuts import render, redirect, get_object_or_404
# 引入User模型
from django.contrib.auth.models import User
# 引入HttpResponse
from django.http import HttpResponse
# 导入数据模型ArticlePost, ArticleColumn
from .models import ArticlePost, ArticleColumn
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入markdown模块
import markdown
# 引入login装饰器
from django.contrib.auth.decorators import login_required
# 引入分页模块
from django.core.paginator import Paginator
# 引入搜索 Q 对象
from django.db.models import Q
# Comment 模型
from comment.models import Comment

from comment.forms import CommentForm

# 通用类视图
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

# Create your views here.

def article_list(request):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        # 按热度排序博文
        article_list = article_list.order_by('-total_views')

    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # 取出文章
    comments = Comment.objects.filter(article=id)

    # 浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    context = {
        'article': article,
        'toc': md.toc,
        'comments': comments
    }

    return render(request, 'article/detail.html', context)


# 检查登录
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户提交数据（POST）
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型需求
        if article_post_form.is_valid():
            # 保存数据，但是暂时不提交到数据库
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            new_article.author = User.objects.get(id=request.user.id)

            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            # 将文章保存到数据库中
            new_article.save()

            # 保存 tags 的多对多关系
            article_post_form.save_m2m()

            # 重定向反向解析到文章列表
            return redirect('article:article_list')
        # 数据不合法，返回错误信息
        else:
            return HttpResponse("表单内有错误，请重新填写。")
    # 用户请求数据（GET）
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()

        columns = ArticleColumn.objects.all()

        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/create.html', context)


# 删除文章
@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("这是你文章吗你就改？？？")
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")


# 安全删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("是你文章吗你就改？？？")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者用户
    if request.user != article.author:
        return HttpResponse("你都不是作者，休想打文章的主意！！！")

    # 判断用户是否为POST提交表单数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型需求
        if article_post_form.is_valid():
            # 保存新写入的 title, body 数据
            article.title = request.POST['title']
            article.body = request.POST['body']

            if request.POST['column'] != 'none':
                # 保存文章栏目
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get['avatar']

            article.tags.set(*request.POST['tags'].split(','), clear=True)
            article.save()
            # 完成之后返回修改后的文章。需要传入文章的id值
            return redirect('article:article_detail', id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新输入")
    # 如果用户时GET请求
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()

        # 文章栏目
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
        }

        # 将响应返回模板
        return render(request, 'article/update.html', context)
