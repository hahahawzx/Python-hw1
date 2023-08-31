from django.shortcuts import render
from .models import article, Comment
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
import random
# Create your views here.
def article_text(request, id): # 这里 request 是 HttpRequest 类型的对象
    article_get = article.objects.get(id=id) # 数据库查询操作
    template = loader.get_template('article/body.html')
    article_content = []
    article_content = article_get.article_content.split('|')
    article_img = []
    if article_get.image_url:
        article_img = article_get.image_url.split('|')
    article_keyword = []
    if article_get.keywords:
        article_keyword = article_get.keywords.split('|')
    
    context = {
        'article_id': id,
        'article_title': article_get.title,
        'article_content': article_content,
        'article_creation':article_get.creation_time.date,
        'article_img':article_img,
        'article_source':article_get.news_website,
        'article_keyword':article_keyword,
        'article_web':article_get.webpage,
        'article_author':article_get.author,
        'Managing_Editor':article_get.Managing_Editor,
        'comments': article_get.comments.all() # 通过外键反向查询
    }
    return HttpResponse(template.render(context, request)) # 返回渲染好的html

def comment(request, id): 
    data = request.POST
    # 将新的消息添加到数据库中
    user = data['user']
    comment_content = data['content']
    article_text = article.objects.get(id=id)
    obj = Comment(article=article_text, user=user, comment_content=comment_content )
    obj.full_clean() #对数据进行验证
    obj.save() #存储在表中
    return HttpResponseRedirect(f'/news_article/article/{id}') # 将页面重定向到博客的url

def delete_comment(request, id):
    data = request.POST
    # 将新的消息添加到数据库中
    comment_id = data['comment_id']
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponseRedirect(f'/news_article/article/{id}') # 将页面


def Homepage(request):
    random_numbers = [random.randint(1, 5500) for _ in range(20)]
    article_list = []
    for i in random_numbers:
        article_get = article.objects.get(id=i) # 数据库查询操作
        article_contents = []
        article_contents = article_get.article_content.split('|')
        contents=''
        for content in article_contents:
            contents = contents + content
    
        context = {
        'article_id': i,
        'article_title': article_get.title,
        'article_content': contents,
        'article_creation':article_get.creation_time.date,
        'article_web':article_get.webpage,
        'comments_count': article_get.comments.count(), # 通过外键反向查询
        'likes':article_get.Likes,
        'favorite':article_get.Favorite,
        }
        article_list.append(context)
    context = {
        "article_list" : article_list
    }
    template = loader.get_template('article/homepage.html')
    return HttpResponse(template.render(context, request))

def news_list(request, id): # 这里 request 是 HttpRequest 类型的对象
    first_id = (id-1)*20+1
    last_id = min(article.objects.count(),(id-1)*20+20)+1
    article_list = []
    for i in range(first_id,last_id):
        article_get = article.objects.get(id=i) # 数据库查询操作
        article_contents = []
        article_contents = article_get.article_content.split('|')
        contents=''
        for content in article_contents:
            contents = contents + content
    
        context = {
        'article_id': i,
        'article_title': article_get.title,
        'article_content': contents,
        'article_creation':article_get.creation_time.date,
        'article_web':article_get.webpage,
        'comments_count': article_get.comments.count(), # 通过外键反向查询
        'likes':article_get.Likes,
        'favorite':article_get.Favorite,
        }
        article_list.append(context)
    firstpage = 1
    lastpage = article.objects.count()//20+1
    context = {
        "article_list" : article_list,
        "page_num":id,
        "firstpage":firstpage,
        "lastpage": lastpage
    }
    template = loader.get_template('article/news_list.html')
    return HttpResponse(template.render(context, request))