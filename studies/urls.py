from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudyFavoriteView, StudyViewSet

router = DefaultRouter()
router.register(r'', StudyViewSet)

urlpatterns = [
    path('favorite/', StudyFavoriteView.as_view(), name='StudyFavorite'), # 즐겨찾기
    path('', include(router.urls)),
]