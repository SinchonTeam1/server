from django.shortcuts import render
from rest_framework import viewsets
from .models import Study, StudyFavorite
from .serializers import StudySerializer, StudyFavoriteSerializer

from rest_framework import permissions
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from threading import Lock
lock = Lock()

# Create your views here.

# 스터디 CRUD 기능
class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = [permissions.IsAuthenticated]

class StudyFavoriteView(APIView):

    # 즐겨찾기 조회
    def get(self,request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = request.user.id

        favorite_study_ids = StudyFavorite.objects.filter(user_id=user_id).values_list('study_id',flat=True)
        data = Study.objects.filter(study_id__in=favorite_study_ids)
        study_list = list(data.values())

        # 즐찾 여부 추가
        for study in study_list:
            study["is_favorite"] = True
        
        response_data = {
            "favorite_list":study_list,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    # 즐겨찾기 등록
    def post(self,request):
        with lock:
            user_id = request.user.id
            study_id = request.data.get('study_id')

            check = StudyFavorite.objects.get(user_id=user_id,study_id=study_id)
            if check:
                return Response({"detail": "the study is already favotirte"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not study_id:
                return Response({"detail": "study_ids are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            dict = {"study_id":study_id, "user_id":user_id}
            serializer = StudyFavoriteSerializer(data=dict)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "info":"즐겨찾기 등록 성공",
                }
                return Response(response_data,status=status.HTTP_200_OK)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    # 즐겨찾기 삭제
    def delete(self,request):
        with lock:
            user_id = request.user.id
            study_id = request.data.get('study_id')

            try:
                favorite = StudyFavorite.objects.get(user_id=user_id,study_id=study_id)
                favorite.delete()

                response_data = {
                    "info":"즐겨찾기 삭제 성공",
                }
                return Response(response_data,status=status.HTTP_200_OK)
            
            except StudyFavorite.DoesNotExist:
                return Response({"detail": "Favorite exam not found"}, status=status.HTTP_400_BAD_REQUEST)