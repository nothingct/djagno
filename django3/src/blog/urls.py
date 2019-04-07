'''
Created on 2019. 4. 6.

@author: 405-2
'''
from blog.views import *
from django.urls.conf import path
from django.views.generic.detail import DetailView
app_name = 'blog'

urlpatterns =[
    #뷰 클래스는 as_view 함수를 호출해서 URL을 등록
    #127.0.0.1:8000/blog
    path('', Index.as_view() , name = 'index'),
    #DetailView 제네릭 뷰는 pk라는 추가 매개변수를 사용함 
    #127.0.0.1:8000/blog/게시물숫자
    path('<int:pk>', Detail.as_view(), name = 'detail'),
    #127.0.0.1:8000/blog/posting
    path('posting/',Posting.as_view(),name ='posting'),
    ]