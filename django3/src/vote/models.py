from django.db import models

# Create your models here.
# 지난번 북마크는 하나의 모델클래스 이번에는 두 개의 모델클래스를 만들고 붙여보기 
#질문  을 위한 클래스 (Question)
#질문 제목(CharField(100글자제한) , 생성일(DateField)을 저장하는 변수들을 포함
#title , pub_date
class Question(models.Model): 
    title = models.CharField('제목',max_length = 100)
    pub_date = models.DateField()
    def __str__ (self):
        return self.title
    #모델클래스에 정의된 변수, 테이블 이름 등을 처리할 때 사용 
    class Meta:
        #ordering : 해당 모델클래스의 객체들을 정렬하는 방식을 지정
        #리스트 형태로 정렬에 사용할 변수이름을 문자열로 작성
        #변수이름 앞에 - 를 붙이면 내림차순으로 정렬 
        
        ordering=['-pub_date']
#답변 을 위한 클래스 (Choice)
#답변 항목 내용, 투표 수, 어떤 질문에 연결되어있는 지를 저장하는 변수들을 포함
#name(CharField(50글자 제한)) , votes(IntegerField) 
#q(ForeignKey(질문 모델 클래스와의 연결)) 
class Choice(models.Model):
    name = models.CharField('답변',max_length = 50)
    #default : 객체 생성 시 기본값 설정하는 매개변수
    votes = models.IntegerField(default = 0)
    #Choice 모델 클래스가 Question 모델 클래스와 1: n 관계를 가짐
    #Question 객체가 삭제되면 연결된 choice 객체도 삭제됨(CASCADE)
    q =  models.ForeignKey(Question, on_delete = models.CASCADE)
    def __str__ (self):
        return self.name
    #ForeignKey : 다른 모델클래스의 객체와 연결할 수 있는 할 수 있는 클래스 
    #ForeignKey(연결할 다른 모델클래스 , on_delete = 삭제방식) 
    #Choice 모델클래스의 q변수는 연결된 Question객체와 동일함 
    #-> Choice객체.q.title(또는 pub_date, id)변수를 접근할 수 있음 
    #on_delete: 연결된 모델클래스의 객체가 살제될때 어떻게 처리할지 저장하는 함수
    #on_delete = models.PROTECT : 연결된 모델클래스의 객체가 삭제되 지 않도록 막아주는 기능 
    #models.CASCADE : 연결된 모델클레스의 객체가 삭제되면 같이 삭제 
    #ex) 글을 삭제하면 글안에 댓글이 사라짐
    #models.SET_NULL: 연결된 객체가 사라지면 아무것도 연결하지 않은 상태 유지 
    #models.SET(연결할 객체) 연결된 객체가 삭제되면 매개변수로 넣은 객체와 연결
    #models.SET_DEFAULT : 연결된 객체가 삭제되면 기본설정된 객체와 연결
    