from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from .models import Category, BiologyContent
from .serializers import CategorySerializer, BiologyContentSerializer, UserSerializer
from .permissions import IsTeacher, IsAuthor  
from .filters import BiologyContentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

User = get_user_model()

# Auth Views
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer  # Reusing for simplicity; could use a dedicated LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': getattr(user, 'role', 'student'),  # assumes your User model has `role`
                }
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


# Category Views
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryContentView(generics.ListAPIView):
    serializer_class = BiologyContentSerializer

    def get_queryset(self):
        category_id = self.kwargs['pk']
        return BiologyContent.objects.filter(category_id=category_id)

# Content Views
class BiologyContentListView(generics.ListCreateAPIView):
    serializer_class = BiologyContentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BiologyContentFilter
    search_fields = ['title', 'content_body']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'teacher':
            return BiologyContent.objects.filter(author=user)
        return BiologyContent.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacher()]
        return []

class BiologyContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BiologyContent.objects.all()
    serializer_class = BiologyContentSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsTeacher(), IsAuthor()]
        return []

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'teacher':
            return BiologyContent.objects.filter(author=user)
        return BiologyContent.objects.filter(is_published=True)