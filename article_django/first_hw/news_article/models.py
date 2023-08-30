from django.db import models
# Create your models here.
class article(models.Model):
    title = models.CharField(max_length=30)
    article_content = models.CharField(max_length=5000,default="Default content")  
    creation_time = models.DateTimeField()
    webpage = models.CharField(max_length=50)
    image_url = models.CharField(max_length=2000,null=True, blank=True)
    keywords= models.CharField(max_length=200,null=True, blank=True) 
    news_website = models.CharField(max_length=30,null=True, blank=True)
    author = models.CharField(max_length=15,null=True, blank=True)
    Managing_Editor = models.CharField(max_length=15,null=True, blank=True)
class Comment(models.Model):
        article = models.ForeignKey(article, on_delete=models.CASCADE) # 将Blog作为外键，Blog删除时级联删除所有的Comment
        user = models.CharField(max_length=10)
        comment_content = models.CharField(max_length=1000)
        creation_time = models.DateTimeField()