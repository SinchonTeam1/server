from .views import *
from django.urls import path

app_name='details'

urlpatterns=[
    path('<int:pk>/', DetailView.as_view()),
]