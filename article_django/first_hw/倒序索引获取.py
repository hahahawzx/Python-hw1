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

inverted_index = {}  

for object in article.objects.all():
    words = jieba.lcut(object.article_content) 
    for word in words:
        if word != "|":
            if word not in inverted_index :
                inverted_index[word] = []
            if object.id not in inverted_index[word]:
                inverted_index[word].append(object.id)  

with open("inverted_index.json", "w") as file:
    json.dump(inverted_index, file)
