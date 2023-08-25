from django.shortcuts import render
from rest_framework import viewsets
from .models import Study, StudyFavorite
from .serializers import StudySerializer, StudyFavoriteSerializer

from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
# from threading import Lock
# lock = Lock()

# Create your views here.

# 스터디 CRUD 기능
class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = [permissions.IsAuthenticated]


class StudyFavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 즐겨찾기 조회
    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        favorite_study_ids = StudyFavorite.objects.filter(user_id=user_id).values_list('study_id',flat=True)
        data = Study.objects.filter(id__in=favorite_study_ids)
        study_list = list(data.values())

        # 즐찾 여부 추가
        for study in study_list:
            study["is_favorite"] = True
        
        return Response(study_list, status=status.HTTP_200_OK)
    
    # 즐겨찾기 등록, 삭제
    def post(self,request):
        user = request.user
        study_id = request.data.get('study_id')
        study = Study.objects.get(id=study_id)

        check, created = StudyFavorite.objects.get_or_create(user_id=user, study_id=study)
        if not created:
            check.delete()
            return Response({"detail": "즐겨찾기 삭제 완료"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StudyFavoriteSerializer(check)
        return Response(serializer.data, status=status.HTTP_200_OK)