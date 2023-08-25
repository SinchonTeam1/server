from django.shortcuts import render
from rest_framework import viewsets
from .models import Study
from .serializers import StudySerializer

# Create your views here.

# 스터디 CRUD 기능
class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer