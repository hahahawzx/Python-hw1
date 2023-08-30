import json
import re
import os
import django
# 打开文件并读取内容
# 设置DJANGO_SETTINGS_MODULE为你的Django项目的settings模块路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "first_hw.settings")

# 初始化Django
django.setup()
from news_article.models import article
i = 2866
num = 5500
while i<=num:
    with open(f'/home/wawawa/python_summer_term/example/data/{i}.json', 'r') as file:
        date = json.load(file)
    data_pattern = r'/(\d{4}-\d{2}-\d{2})/'
    match = re.search(data_pattern, date['urls']['webpage'])
    if match:
        date['details']['creation_time'] = match.group(1)
    else:
        print("failed")
    # 现在 `data` 变量中包含了 JSON 文件中的数据
    article_text = ""
    for str in date['content']:
        article_text=article_text +'|'+ str 
    keyword = ""
    for str in date['details']['keywords']:
        keyword=keyword +'|'+ str 
    img = ""
    for str in date['urls']['image_url']:
        img=img +'|'+ str 
    new_article = article(
        title=date['title'],
        article_content=article_text,
        creation_time=date['details']['creation_time'], 
        webpage = date['urls']['webpage'],
        image_url = img,
        keywords= keyword, 
        news_website = date['news_website'],
        author = date['author'],
        Managing_Editor = date['Managing Editor']
)
    new_article.save()
    print(i)
    i = i+1
    print(i)
