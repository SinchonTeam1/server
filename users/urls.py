from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, LogoutView, UserView, VerifyEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('list/', UserView.as_view(), name="user"),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),


]