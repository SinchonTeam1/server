from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import EmailVerificationToken
from .serializers import LoginSerializer, UserSerializer

User = get_user_model()
BASE_URL = 'http://127.0.0.1:8000'


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email', '')
        
        if not email.endswith("@sogang.ac.kr") and not email.endswith("@yonsei.ac.kr") and not email.endswith("@g.hongik.ac.kr") and not email.endswith("@ewhain.net"):
            return Response({"message": "잘못된 학교 선택입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        data._mutable = True

        if email.endswith("@sogang.ac.kr"):
            data['school'] = '서강대학교'
        elif email.endswith("@yonsei.ac.kr"):
            data['school'] = '연세대학교'
        elif email.endswith("@g.hongik.ac.kr"):
            data['school'] = '홍익대학교'
        elif email.endswith("@ewhain.net"):
            data['school'] = '이화여자대학교'
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()

        verification_token = EmailVerificationToken.objects.create(user=user)
        
        send_mail(
            '이메일 인증을 완료해주세요!',
            f'이 토큰을 붙여넣기 해주세요: {verification_token.token}',
            'taeho205@likelion.org',
            [user.email],
            fail_silently=False,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if not user.email_verified:
                    return Response({"message": "이메일을 인증해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

                token = TokenObtainPairSerializer.get_token(user)
                access_token = str(token.access_token)
                refresh_token = str(token)
                return Response({
                    "access": access_token,
                    "refresh": refresh_token
                })
            else:
                return Response({"message": "로그인 실패"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            token = request.data.get("token")
            email_token = EmailVerificationToken.objects.get(token=token)
            email_token.user.email_verified = True  # Assuming you have an `email_verified` field in your User model
            email_token.user.save()
            email_token.delete()
            return Response({"message": "이메일 인증 성공"}, status=status.HTTP_200_OK)
        except EmailVerificationToken.DoesNotExist:
            return Response({"error": "Invalid token or token expired"}, status=status.HTTP_400_BAD_REQUEST)
