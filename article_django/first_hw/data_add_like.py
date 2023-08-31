import json
import re
import os
import django
import random
# 打开文件并读取内容
# 设置DJANGO_SETTINGS_MODULE为你的Django项目的settings模块路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "first_hw.settings")

# 初始化Django
django.setup()
from news_article.models import article
for object in article.objects.all():
    object.Favorite = random.randint(1,10000)
    object.Likes = random.randint(1,10000)
    object.save()
