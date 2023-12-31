from .models import Study, StudyFavorite
from .serializers import StudySerializer, StudyFavoriteSerializer, StudyGetSerializer

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# 스터디 CRUD 기능
class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        field = query_params.get("field", "")
        company = query_params.get("company", "")
        
        queryset = self.filter_queryset(self.get_queryset())
        
        if field:
            queryset = queryset.filter(field__icontains=field)
        
        if company:
            queryset = queryset.filter(company__icontains=company)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StudyGetSerializer(queryset, many=True)
        return Response(serializer.data)


class StudyFavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 즐겨찾기 조회
    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        favorite_study_ids = StudyFavorite.objects.filter(user_id=user_id).values_list('study_id',flat=True)
        data = Study.objects.filter(id__in=favorite_study_ids)
        serializer = StudyGetSerializer(data, many=True)

        # # 즐찾 여부 추가
        # for study in study_list:
        #     study["is_favorite"] = True
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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