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
with open('/home/wawawa/python_summer_term/example/data/1.json1.json', 'r') as file:
    date = json.load(file)
data_pattern = r'/(\d{4}-\d{2}-\d{2})/'
match = re.search(data_pattern, date['urls']['webpage'])
if match:
    date['details']['creation_time'] = match.group(1)
    print(date['details']['creation_time'])
else:
    print("failed")
# 现在 `data` 变量中包含了 JSON 文件中的数据