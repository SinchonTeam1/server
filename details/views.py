from django.shortcuts import render
from django.shortcuts import get_object_or_404
from studies.models import *
from studies.serializers import *
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class DetailView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, format=None):
        details=get_object_or_404(Study, pk=pk)
        serializer=StudySerializer(details)
        return Response(serializer.data)