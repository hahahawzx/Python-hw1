from django.urls import path, include
import news_article.views as views

urlpatterns = [
    # path('shouye', views.shouye),
    # path('liebiaoye/<int:id>', views.liebiaoye)
    path('article/delete_comment/<int:id>', views.delete_comment),
    path('article/comment/<int:id>', views.comment),
    path('article/<int:id>',views.article_text),
    path('newslist/<int:id>',views.news_list),
    path('Homepage',views.Homepage),
    path('search',views.search)
    
]