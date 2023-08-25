from .views import *
from django.urls import path

app_name='mypages'

urlpatterns=[
    path('<int:pk>/', MyPageView.as_view()),
]