import json
import re
import os
import django
import random
import jieba
# 打开文件并读取内容
# 设置DJANGO_SETTINGS_MODULE为你的Django项目的settings模块路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "first_hw.settings")

# 初始化Django
django.setup()
from news_article.models import article
object = article.objects.get(id =1)
content = object.article_content
with open('inverted_index.json', 'r') as file:
    data = json.load(file)
words = jieba.lcut(object.article_content)  # 使用jieba分词
total_num =0
article_choose = {} #用字典来存有这些词的文章
for word in words:
    if word in data:
        total_num = total_num+1
        for id in data[word]:
            if id not in article_choose :
                article_choose[id] = 0  
            article_choose[id] = article_choose[id]+1
article_found = []
for id in article_choose:
    if article_choose[id] > 2*total_num/3-1: #以存在三分之二为界限
        article_found.append(id)
print(article_found)
