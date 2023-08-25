from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
# 모든 StudyViewSet 관련 URL은 /studys/로 시작함
router.register(r'studys', views.StudyViewSet)

urlpatterns = [
    path('api/',include(router.urls))
]