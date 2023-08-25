from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views
from .views import *

router = DefaultRouter()
router.register(r'', views.StudyViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('favorite/',StudyFavoriteView.as_view(),name='StudyFavorite'), # 즐겨찾기
]