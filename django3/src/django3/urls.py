"""django3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from bookmark.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='main'),
    #127.0.0.1:8000/vote 로 시작하는 UTL들을 
    #Vote폴더의 urls.py 에서 처리하도록 등록함 
    path('vote/',include('vote.urls')),
    #127.0.0.1:8000/c1 로 시작하는 URL들을 
    #customlogin 폴더의 urps.py 에서 처리허록 등록
    path('cl/',include('customlogin.urls')),
    path('list/', book_list),
    #http://127.0.0.1:8000/숫자/
    #->book_one 뷰호출, book_idx변수에 숫자값이 들어감
    
    #social_django 어플리케이션의 하위URLConf 등록
    #우리가 만든 어플리케이션이 아니므로 app_name 변수에 어떤 값이 있는지 확인하기 힘듦
    #include 함수의 namespace 매개변수 : app_name 변수를 무시하고 하위 그룹의 이름을 지정할수 있음
    path('<int:book_idx>/', book_one),
    path('auth/',include('social_django.urls',namespace = 'social')),
    path('blog/', include('blog.urls'))
]

#사용자가 이미지/ 첨부파일을 요청 하였을 때 
#웹 서버 컴퓨터에 저장된 파일을 클라이언트에게 전달하도록 설정 
#웹서버의 로컬 하드디스크와 URL 주소를 연동 

#setting.py 변수값을 사용할 수 있도록 임포트
from django.conf import settings
#MEDIA_URL 과 MEDIA_ROOT 를 연결하기 위한 함수 임포트 
from django.conf.urls.static import static 

#웹클라이언트의 파일요청 URL 주소와 실제 파일경로를 연동함
urlpatterns += static(settings.MEDIA_URL,
                      document_root = settings.MEDIA_ROOT)

