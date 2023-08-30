import requests # 用于请求
from bs4 import BeautifulSoup as BS # 用于找到东西
from time import sleep # 用于放慢速度
from fake_useragent import UserAgent # 用于生成随机UserAgent
import re #用于正则表达式
import json #用于json解析
import re #正则表达式
import copy #用于深度赋值
import random #用于随机ip

article_templete = {
    "title": "",
    "news_website": "",
    "author": "",
    "Managing Editor": "",
    "details": {
        "creation_time": "",
        # "comments_count": "",
        "keywords": []
    },
    "content": [],
    "urls": {
        "webpage": "",
        "image_url": []
    }
}


# start: helper function---
# image_url

def find_photo_url(element, results):
    aims = element.find_all('div', class_="img_wrapper")
    for aim in aims:
        for child in aim.children:
            if child.name == 'img':
                results.append(child['src'])


# keywords
def find_keywords(element, results):
    aims = element.find_all('div', class_="keywords")
    for aim in aims:
        for child in aim.children:
            if child.name == 'a':
                results.append(child.get_text())


# content

def find_body(element):
    result = element.find_all('div', id="artibody")
    if len(result) == 1:
        return result[0]
    else:
        return None


def find_content(element, results):
    aims = element.find_all(name=['p', 'strong'])
    for aim in aims:
        if len(aim.find_all()) == 0:
            results.append(aim.get_text().replace("\u3000", "").replace("\n", "").replace("\t", "").strip())


# author

def find_author(element, results):
    aims = element.find_all('span', class_="author")
    for aim in aims:
        for child in aim.children:
            if child.name == 'a':
                results.append(child.get_text())


# time
def find_time_1(element, results):
    aims = element.find_all('span', class_="date")
    for aim in aims:
        results.append(aim.get_text())


def find_time_2(element, results):
    aims = element.find_all('span', id="pub_date")
    for aim in aims:
        results.append(aim.get_text())


# end: helper function---------

# start: core function----------
def get_news_data(url):

    # 发送请求
    article = copy.deepcopy(article_templete)
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BS(response.text, "lxml")

    # web url
    article["urls"]["webpage"] = url

    # title
    titles = soup.find_all('title')
    if titles:
        title = titles[0].string.strip().split("_")
        if len(title) > 1:
            article["title"] = title[0].replace("|", "")
            article["news_website"] = title[1].replace("|", "")
        else:
            article["title"] = title[0]
    else:
        print(f"there is no title in the article from this url:{url},maybe something wrong")

    # image_url
    photo_urls = []
    find_photo_url(soup, photo_urls)
    for photo_url in photo_urls:
        article["urls"]["image_url"].append("https:" + photo_url)

    # content and Managing Editor
    contents = []
    body = find_body(soup)
    if body:
        find_content(body, contents)
        for content in contents:
            if "责任编辑：" in content:
                editor_name = content.replace("责任编辑", " ").strip()
                article["Managing Editor"] = editor_name
                contents.remove(content)
            if "文 |" in content:
                author_name = content.replace("文 |", " ").strip()
                article["author"] = author_name.replace("\xa0", "")
                contents.remove(content)
        article["content"] = contents
    else:
        print("cannot find the body")
        # author
    if not article["author"]:
        authors = []
        find_author(soup, authors)
        if len(authors) != 0:
            article["author"] = authors[0]
    # time
    times = []
    find_time_1(soup, times)
    if times:
        article["details"]["creation_time"] = times[0]
    else:
        find_time_2(soup, times)
        if times:
            article["details"]["creation_time"] = times[0].replace("\n", "").strip()
        else:
            print("there is no time")

    # keywords
    keywords = []
    find_keywords(soup, keywords)
    article["details"]["keywords"] = keywords
    return article


# end: core function----------

num = 3000
flag = 0
with open('url_tech.txt', 'r') as file:
    article_list = []
    for line in file:
        if flag >= num:
            break
        else:
            print(flag)
        # 处理每一行的数据
        url = line.strip()  # 输出处理后的行数据（去除行尾的换行符）
        article_list.append(get_news_data(url))
        flag = flag + 1

print(article_list)
with open("data1.json", "w", encoding='utf-8') as json_file:
    json.dump(article_list, json_file, ensure_ascii=False)