from django.shortcuts import render
from django.views.generic.list import ListView
from blog.models import Post, PostImage, PostFile
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

#클래스 기반의 뷰를 만들 때 , 
#제네릭뷰를 상속받아서 장고에서 제공하는 뷰 기능을 사용 
#제네릭 뷰 : 장고에서 제공하는 여러가지 상황별 뷰 기능을 구현한 클래스 

#index : 글목록이 뜨는 메인페이지
#ListView : 특정 모델클래스의 객체 목록을 다루는 기능이 구현된 뷰 
class Index(ListView):
    #사용자에게 전달할 HTML파일 경로
    template_name = 'blog/index.html'
    
    #리스트로 뽑을 모델클래스 지정
    model = Post
    #템플릿에 객체 리스트를 전달할 때 사용할 변수명 
    context_object_name = 'list'
    
    #한페이지에 최대 몇개의 객체가 보여질지 설정 
    paginate_by = 5
    
#detail : 글 상세보기 페이지
#DetailView : 특정 모델클래스 객체 한 개를 추출해서 템플릿에 넘겨주는 제네릭 뷰  

#DetailView는 requset 외에 추가 매개변수를 사용해 추출할 객체를 찾음
#-> pk 변수 : id값 같은 고유값으로 객체를 찾을때 사용
class Detail(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    context_object_name= 'obj'
#posting : 글쓰기 페이지 

#FormView 에서 사용할 폼클래스 임포트
from blog.forms import PostForm
#Posting : 글쓰기 페이지 
#FormView : 특정 폼클래스를 다루는 기능이 구현된 제네릭뷰
#LoginRequiredMixin : 사용자가 비로그인 상태로 이 뷰를 요청한
#경우 , 로그인 페이지로 이동해주는 클래스
#뷰함수 -> 데코레이터, 뷰클래스-> XXXMixin 클래스 상속
class Posting(LoginRequiredMixin,FormView):
    template_name = 'blog/posting.html'
    #해당 뷰클래스가 사용할 폼 클래스 지정
    form_class = PostForm
    context_object_name = 'f'
    
    #is_valid() 함수가 True 값을 반환한 뒤의 처리를 form_valid() 에서 함
    #사용자가 춘 추가데이터(이미지,파일정보) 를 처리하기 위해서 해당함수를 오버라이딩 
    #form 매개변수 : form_class변수에 지정한 폼클래스 객체가 저장됨 
    def form_valid(self, form):
        #PostForm 객체를 저장하기 전에 글쓴이 정보를 저장해야 함. 
        #데이터베이스에 바로저장하지 않고 연동된 모델클래스로 변환.
        #p 사용자 입력으로 제목, 카테고리 , 글 내용이 채워진 Post객체
        #(아직 데이터베이스에 저장되지 않음. )  
        p = form.save(commit = False);
        #request.user : 요청한 클라이언트의 로그인 정보 
        #        (User모델 클래스 객체) 
        #이 요청을 한 클라이언트의 유저정보를 Post 객체에 저장 
        p.author = self.request.user
        p.save() # 데이터베이스에 저장
        
        #사용자가 넘겨준 이미지, 파일마다 객체 생성 
        #사용자가 넘겨준 이미지 파일마다 PostImage 객체 생성
        #request.FILES : 클라이언트가 서버로 보낸 파일정보를 관리하는변수 ( 객체형태 ) 
        
        #f : 사용자가 보낸 이미지파일의 실제정보 
        for f in self.request.FILES.getlist('images'):
            #새로운 PostImage 객체를 생성 (데이터베이스에 저장 X) 
            pi = PostImage()
            # 이 요청으로 새로 만들어진 Post객체 와 연결
            pi.post = p
            #사용자가 보낸 이미지 파일 정보를 변수에 저장 
            pi.image = f
            pi.save() #데이터 베이스에 새로운 PostImage객체 저장
           
            #사용자가 넘겨준 첨부파일 마다 PostFile 객체 생성
        for f in self.request.FILES.getlist('files'):
            #새로운 PostImage 객체를 생성 (데이터베이스에 저장 X) 
            pf = PostFile()
            # 이 요청으로 새로 만들어진 Post객체 와 연결
            pf.post = p
            #사용자가 보낸 이미지 파일 정보를 변수에 저장 
            pf.file = f
            pf.save() #데이터 베이스에 새로운 PostImage객체 저장
            #완성된 글의 URL을 전달
            return HttpResponseRedirect(
                reverse('blog:detail',args = (p.id,))
            )
        return p