from django.shortcuts import render
from .models import article, Comment
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.db.models import Q
import random
import json
import jieba
from django.views.decorators.csrf import csrf_exempt
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
        'source':article_get.news_website,
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
        'source':article_get.news_website,
        }
        article_list.append(context)
    firstpage = 1
    if article.objects.count()% 20 !=0:
        lastpage = article.objects.count()//20+1
    else:
        lastpage = article.objects.count()//20
    context = {
        "article_list" : article_list,
        "page_num":id,
        "firstpage":firstpage,
        "lastpage": lastpage
    }
    template = loader.get_template('article/news_list.html')
    return HttpResponse(template.render(context, request))


def search(request): 
    start_time =  datetime.now()
    data = request.POST
    choose = data['choose'] 
    comment_content = data['content']  
    page_num = int(data['page_num'])

    #查找文章的操作，不可能有问题
    with open('inverted_index.json', 'r') as file:
        data = json.load(file)
    words = jieba.lcut(comment_content)  # 使用jieba分词
    total_num =0
    article_choose = {} #用字典来存有这些词的文章
    for word in words:
        if word in data:
            total_num = total_num+1
            for id_list in data[word]:
                if id_list not in article_choose :
                    article_choose[id_list] = 0  
                article_choose[id_list] = article_choose[id_list]+1
    # 获取查询集合
    article_ids = [
        id_select for id_select in article_choose
        if article_choose[id_select] > 2 * total_num / 3 - 1
    ]
    #tag获取
    tag_sum = 0
    if 'tag1' in request.POST: #创事记
       tag_sum = tag_sum+1
    if 'tag2' in request.POST: #新浪科技
        tag_sum = tag_sum+2
    if 'tag3' in request.POST: #新浪财经
        tag_sum = tag_sum+4
    if 'tag4' in request.POST: #其他
        tag_sum = tag_sum+8
    if 'tag_sum' in request.POST:
        tag_sum = int(request.POST['tag_sum'])
    if tag_sum == 0:
        tag_sum = 15
    #tag获取
    #tag筛选
 
    #tag筛选
    #排序
    if choose == "time":
        sorted_articles = article.objects.filter(id__in=article_ids).order_by('-creation_time')
    else:
        sorted_articles = article.objects.filter(id__in=article_ids).order_by('-Likes')
    #排序
    
    # 现在id列表中的就是搜索到的
    first_id = min((page_num-1)*20,len(sorted_articles))
    last_id = min(len(sorted_articles)-1,(page_num-1)*20+20)+1
    article_list = []
    for i in range(first_id,last_id):
        article_get = sorted_articles[i] # 数据库查询操作
        article_contents = []
        article_contents = article_get.article_content.split('|')
        contents=''
        for content in article_contents:
            contents = contents + content
    
        context = {
        'article_id': article_get.id,
        'article_title': article_get.title,
        'article_content': contents,
        'article_creation':article_get.creation_time.date,
        'article_web':article_get.webpage,
        'comments_count': article_get.comments.count(), # 通过外键反向查询
        'likes':article_get.Likes,
        'favorite':article_get.Favorite,
        'source':article_get.news_website,
        }
        article_list.append(context)
    firstpage = 1
    if len(sorted_articles)% 20 !=0:
        lastpage = len(sorted_articles)//20+1
    else:
        lastpage = len(sorted_articles)//20
    end_time = datetime.now()
    time_difference = end_time - start_time
    context = {
        "article_list" : article_list,
        "total_num":len(sorted_articles),
        "question" : comment_content,
        "total_time":time_difference.total_seconds(),
        "page_num":page_num,
        "firstpage":firstpage,
        "lastpage": lastpage,
        'choose': choose,
        "comment_content": comment_content,
        'tag_sum':tag_sum,
    }
    
    template = loader.get_template('article/search.html')
    return HttpResponse(template.render(context, request))



def classify(request):
    csj_sum = article.objects.filter(news_website="创事记").count()
    xlcj_sum = article.objects.filter(news_website="新浪财经").count()
    xlkj_sum = article.objects.filter(news_website="新浪科技").count()
    query = Q(news_website="科技频道") | Q(news_website="新浪网")
    qt_sum = article.objects.filter(query).count()
    csj = {
        "name" :"创事记",
        "sum" : csj_sum,
        "shortening":"csj",
        }
    xlcj = {
        "name" :"新浪财经",
        "sum" : xlcj_sum,
        "shortening":"xlcj",
      }
    xlkj = {
        "name" :"新浪科技",
        "sum" : xlkj_sum,
        "shortening":"xlkj",
      }
    qt = {
        "name" :"其他",
        "sum" : qt_sum,
        "shortening":"qt",
      }
    item = []
    item.append(csj)
    item.append(xlcj)
    item.append(xlkj)
    item.append(qt) 
    context = {
       "items":item
    }
    template = loader.get_template('article/classify.html')
    return HttpResponse(template.render(context, request))

def csj(request,id):
    csj_article = article.objects.filter(news_website="创事记")
    first_id = (id-1)*20
    last_id = min(article.objects.filter(news_website="创事记").count(),(id-1)*20+20)
    article_list = []
    for i in range(first_id,last_id):
        article_get = csj_article[i]
        article_contents = []
        article_contents = article_get.article_content.split('|')
        contents=''
        for content in article_contents:
            contents = contents + content
    
        context = {
        'article_id': article_get.id,
        'article_title': article_get.title,
        'article_content': contents,
        'article_creation':article_get.creation_time.date,
        'article_web':article_get.webpage,
        'comments_count': article_get.comments.count(), # 通过外键反向查询
        'likes':article_get.Likes,
        'favorite':article_get.Favorite,
        'source':article_get.news_website,
        }
        article_list.append(context)
    firstpage = 1
    if article.objects.filter(news_website="创事记").count()% 20 !=0:
        lastpage = article.objects.filter(news_website="创事记").count()//20+1
    else:
        lastpage = article.objects.filter(news_website="创事记").count()//20
    context = {
        "article_list" : article_list,
        "page_num":id,
        "firstpage":firstpage,
        "lastpage": lastpage
    }
    template = loader.get_template('article/csj.html')
    return HttpResponse(template.render(context, request))

def xlkj(request,id):
    xlkj_article = article.objects.filter(news_website="新浪科技")
    first_id = (id-1)*20
    last_id = min(article.objects.filter(news_website="新浪科技").count(),(id-1)*20+20)
    article_list = []
    for i in range(first_id,last_id):
        article_get = xlkj_article[i]
        article_contents = []
        article_contents = article_get.article_content.split('|')
        contents=''
        for content in article_contents:
            contents = contents + content
    
        context = {
        'article_id': article_get.id,
        'article_title': article_get.title,
        'article_content': contents,
        'article_creation':article_get.creation_time.date,
        'article_web':article_get.webpage,
        'comments_count': article_get.comments.count(), # 通过外键反向查询
        'likes':article_get.Likes,
        'favorite':article_get.Favorite,
        'source':article_get.news_website,
        }
        article_list.append(context)
    firstpage = 1
    if article.objects.filter(news_website="新浪科技").count()% 20 !=0:
        lastpage = article.objects.filter(news_website="新浪科技").count()//20+1
    else:
        lastpage = article.objects.filter(news_website="新浪科技").count()//20
    context = {
        "article_list" : article_list,
        "page_num":id,
        "firstpage":firstpage,
        "lastpage": lastpage
    }
    template = loader.get_template('article/xlkj.html')
    return HttpResponse(template.render(context, request))


def xlcj(request,id):
    xlcj_article = article.objects.filter(news_website="新浪财经")
    first_id = (id-1)*20
    last_id = min(article.objects.filter(news_website="新浪财经").count(),(id-1)*20+20)
    article_list = []
    for i in range(first_id,last_id):
        article_get = xlcj_article[i]
        article_contents = []
        article_contents = article_get.article_content.split('|')
        contents=''
        for content in article_contents:
            contents = contents + content
    
        context = {
        'article_id': article_get.id,
        'article_title': article_get.title,
        'article_content': contents,
        'article_creation':article_get.creation_time.date,
        'article_web':article_get.webpage,
        'comments_count': article_get.comments.count(), # 通过外键反向查询
        'likes':article_get.Likes,
        'favorite':article_get.Favorite,
        'source':article_get.news_website,
        }
        article_list.append(context)
    firstpage = 1
    if article.objects.filter(news_website="新浪财经").count()% 20 !=0:
        lastpage = article.objects.filter(news_website="新浪财经").count()//20+1
    else:
        lastpage = article.objects.filter(news_website="新浪财经").count()//20
    context = {
        "article_list" : article_list,
        "page_num":id,
        "firstpage":firstpage,
        "lastpage": lastpage
    }
    template = loader.get_template('article/xlcj.html')
    return HttpResponse(template.render(context, request))

def qt(request,id):
    query = Q(news_website="科技频道") | Q(news_website="新浪网")
    qt_article = article.objects.filter(query)
    first_id = (id-1)*20
    last_id = min(article.objects.filter(query).count(),(id-1)*20+20)
    article_list = []
    for i in range(first_id,last_id):
        article_get = qt_article[i]
        article_contents = []
        article_contents = article_get.article_content.split('|')
        contents=''
        for content in article_contents:
            contents = contents + content
    
        context = {
        'article_id': article_get.id,
        'article_title': article_get.title,
        'article_content': contents,
        'article_creation':article_get.creation_time.date,
        'article_web':article_get.webpage,
        'comments_count': article_get.comments.count(), # 通过外键反向查询
        'likes':article_get.Likes,
        'favorite':article_get.Favorite,
        'source':article_get.news_website,
        }
        article_list.append(context)
    firstpage = 1
    if article.objects.filter(query).count()% 20 != 0:
        lastpage = article.objects.filter(query).count()//20+1
    else:
        lastpage = article.objects.filter(query).count()//20
    context = {
        "article_list" : article_list,
        "page_num":id,
        "firstpage":firstpage,
        "lastpage": lastpage
    }
    template = loader.get_template('article/qt.html')
    return HttpResponse(template.render(context, request))