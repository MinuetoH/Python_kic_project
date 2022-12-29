from django.db import models

# Create your models here.
# python manage.py makemigrations => models.py 수정시 반드시 해야함
# python manage.py migrate
# mariadb에서 member_member 테이블 확인

class Member(models.Model) :
    id = models.CharField(max_length=20,primary_key=True)
    pass1=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    gender=models.IntegerField(default=0)
    tel=models.CharField(max_length=20)
    email=models.CharField(max_length=100)
    picture=models.CharField(max_length=200)
    
    #def __repr__(self) : 같은 함수
    def __str__(self) :
        return self.id + ":" + self.name + ":" + self.pass1
    
class UserDB(models.Model) :
    id = models.CharField(max_length=20,primary_key=True)
    pass1=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=100)
    
    #def __repr__(self) : 같은 함수
    def __str__(self) :
        return self.id + ":" + self.name + ":" + self.pass1