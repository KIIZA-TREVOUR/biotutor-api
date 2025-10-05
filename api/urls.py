from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'), 
    path('content/', views.BiologyContentListView.as_view(), name='content-list'),
    path('content/<int:pk>/', views.BiologyContentDetailView.as_view(), name='content-detail'),
]