'''
<form> : HTML 의 <form> 태그로 사용자가 웹서버에게 전달할 값들을 작성할 수 있는 공간을 생성
<form> 태그 안의 <input> 태그를 작성 --> 어떤 입력을 할 수 있는지 지정할 수 있게함
form 태그의 속성으로 action, method 를 지정해야 한다. 
action : 사용자의 입력을 웹서버의 어느 URL 로 보낼 것인지에 대한 지정
method : GET or POST

장고의 form : HTML 의 <form> 태그에 들어가는 <input>태그들을 관리할 수 있는 클래스 / 기능 
모델클래스에 정의된 변수에 맞춰 <input> 을 자동생성하거나 커스텀 입력공간도 생성할 수 잇음. 
'''

from django.forms.models import ModelForm
from vote.models import Question, Choice
'''
ModelForm : 모델클레스를 기반으로 입력양식을 자동생성할 떄 상속받는 클래스
Form : 커스텀 입력양식을 생성할 때 상속받는 클래스 

기존의 기능 개발순서 
Model 클래스 정의 -> 뷰 함수/ 클래스 정의 -> HTML 코드 작성 -> URL Conf 등록

변경 
Model 클래스 정의 -> form 클래스 정의 -> 뷰 함수/ 클래스 정의 -> HTML 코드 작성 -> URL Conf 등록

'''

#Question 모델클래스 와 연관된 모델폼 클래스 정의 
#Question 객체 추가 / 수정 떄 사용
class QuestionForm(ModelForm):
    #Meta 클래스 : 연동하고자 하는 모델클래스에 대한 정보를 정의하는 클래스 ( 대문자 주의 0 
    class Meta:
        model =  Question    # 이 모델폼클래스가 Question 모델클래스와 연동
        fields = [ 'title' ] # Question 모델클래스의 변수중 title 변수만 작성 가능 
        #model, fields , exlude - 변수이름 주의 
        #model : 연동하고자 하는 모델클래스를 지정 
        #fields : 해당하는 모델클레스에 정의된 변수 중 어떤 변수를 클라이언트가 입력할 수 있는지 지정하는 변수
        #(iterable, list 형태로 변수명을 문자열로 저장함 ) 
        #exclude : 해당하는 모델클레스에 정의된 변수 중 어떤 변수를 클라이언트가 작성할 수 없는지 지정
        #fields 나 exclude 중 하나만 사용 
        
#Choice 모델클래스와 연동된 모델폼 클래스 정의 
#Choice 객체 추가/ 수정 때 사용 
class ChoiceForm(ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        print(self.fields)
        self.fields['q'].label = '설문조사'
    class Meta:
        model = Choice
        fields = ['name' , 'q' ]
        exclude = []