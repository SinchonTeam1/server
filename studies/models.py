from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Study(models.Model):
    title = models.CharField(max_length=100) # 제목
    created_at = models.DateField(auto_now_add=True) # 게시일
    deadline = models.DateField() # 마감일
    writer = models.ForeignKey(User,on_delete=models.CASCADE) # 작성자 정보
    members = models.ManyToManyField(User, related_name='studies') # 참여자 정보
    numbers = models.IntegerField() # 모집인원
    period = models.DurationField() # 예상기간
    start = models.DateField() # 시작예정일
    contact = models.CharField(max_length=100) # 연락 방법
    field = models.CharField(max_length=100) # 분야
    company = models.CharField(max_length=100)# 회사
    content = models.TextField() # 스터디 소개글

class StudyFavorite(models.Model):
    study_id = models.ForeignKey(Study, on_delete=models.CASCADE,null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)