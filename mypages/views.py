from django.shortcuts import render
from django.shortcuts import get_object_or_404
from users.models import *
from users.serializers import *
from rest_framework import views
from rest_framework.response import Response
from studies.models import Study
from studies.serializers import StudySerializer
# Create your views here.

class MyPageView(views.APIView):

    #게시한 스터디 
    def get(self, request, *args, **kwargs):
        user = request.user
        studies = Study.objects.filter(writer=user)
        serializer = StudySerializer(studies, many=True)
        return Response(serializer.data)
