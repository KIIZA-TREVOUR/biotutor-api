from django.shortcuts import render
from rest_framework import generics
from .models import  Category, BiologyContent
from .serializers import CategorySerializer, BiologyContentSerializer
from django_filters.rest_framework import DjangoFilterBackend  
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsTeacher, IsAuthor
from .filters import BiologyContentFilter  

# Create your views here.

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BiologyContentListView(generics.ListCreateAPIView):
    serializer_class = BiologyContentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BiologyContentFilter 
    search_fields = ['title', 'content_body']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        # Students see only published content
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