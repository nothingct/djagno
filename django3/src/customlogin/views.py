from django.shortcuts import render
from django.contrib.auth.models import User
from customlogin.forms import SignupForm,SigninForm
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
# Create your views here.
#회원가입
#GET - 회언가입 입력할 수 있는 HTML파일 제공 
#POST - 사용자 입력 기반의 회원생성
def signup(request):
    if request.method == 'GET':
        
        f = SignupForm()
        return render(request , 'cl/signup.html' ,{ 'form':f} )
    elif request.method == 'POST':
        f = SignupForm(request.POST)
        #유호한 값으로 채워져 있는지 확인
        #(아이디 중복, 비밀번호 형식이 올바른지, 이메일 
        if f.is_valid():
            #is_valud 가 True 인경우 cleaned_data 변수로
            #사용자의 입력을 추출할 수 잇음 
            #비밀번호 확인한과 비밀번호가 같은지 확인
            if f.cleaned_data['password_check'] == f.cleaned_data['password']:
                
                
            #회원생성
            
            # User   : auth 어플리케이션에 구현된 모델클래스
            #User.objects.create_user : 비밀번호 를 암호화 한 상태로 회원을 생성하는 함수
        
                
                new_user = User.objects.create_user(username= f.cleaned_data['username'], 
                                                    email= f.cleaned_data['email'],
                                                    password=f.cleaned_data['password'])
                print('새 유저 : ',new_user)
                new_user.last_name = f.cleaned_data['last_name']
                new_user.first_name = f.cleaned_data['first_name']
                #수정사항(성, 이름 변수에 값 변경 ) 을 데이터베이스에 반영
                new_user.save()
                # 회원 생성 완료  HTML 전달
                return render(request,'cl/signupcom.html',
                              {'name' : new_user.username})
            #비밀 번호 입력이 다른 경우에 대한 처리 
            else:
                return render(request, 'cl/signup.html',
                              {'form':f, 'error': '비밀번호가 다릅니다.'} )
            
        #유효하지 않은 입력값이 있을 때의 처리 else:
        else:
            return render(request, 'cl/signup.html',
                              {'form':f, 'error': '형식 이 맞지 않습니다.'})
#로그인 
#GET - 로그인에 관한 입력을 할 수 있는 HTML 전달
#POST - 사용자 입력과 같은 회원이 존재하는지 확인 후 로그인 
def signin(request):
    if request.method == "GET":            
        f=SigninForm()
        return render(request,'cl/signin.html', {'form' : f} )
    elif request.method =="POST":
        #회원 조회 하는 함수를 사용해 아이디와 비밀번호가 동일 한 회원이 있는지 확인. 
        #is_valid 를 사용해 유효성 검사를 할 경우 
        #아이디 중복에 걸려 항상 False 가 뜸
        #따라서 오류가 발생했을 때 입력을 전달하기 위한 폼객체 생성
        f= SigninForm(request.POST)
        #POST 변수에서 직접 데이터 꺼내기 (아이디, 비밀번호) 
        id = request.POST.get('username')
        pw = request.POST.get('password')
        #아이디랑 비밀번호가 일치하는 User 모델클래스 객체 추출 
        #authenticate(username, password) : 비밀번호를 암호화하고 
        #아이디 와 암호화된비밀번호가 일치하는 User 객체 추출
        #단, 아이디나 비밀번호가 틀린 경우, None 값을 반환함
        u = authenticate(username = id, password = pw)
        #회원 정보가 u 변수에 들어있는 경우 
        if u :
            #로그인 처리 
            #login(request, u) : 해당 뷰를 요청한 클라이언트가
            #u 에 저장된 user 객체 정보를 저장하는 함수
            login(request, u)
            #nexturl : 이동할 url 주소를 저장하는 변수 
            nexturl = request.POST.get('nexturl')
            if nexturl: 
                return HttpResponseRedirect(nexturl)
            else:
                return HttpResponseRedirect(reverse('vote:index'))
        #회원 정보가 u 변수에 없는 경우(None)
        else : 
            return render(request,'cl/signin.html',{'form' : f, 'error':'아이디 또는 비밀번호가 틀렸습니다.'})
#로그아웃
def signout(request):
    #logout(request) : 요청한 클라이언트의 User 저장 변수 값을 삭제함
    logout(request)
    return HttpResponseRedirect(reverse('cl:signin'))
