from .views import *
from django.urls import path

app_name='mypages'

urlpatterns=[
    path('', MyPageView.as_view()),
]