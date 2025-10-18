from django.urls import path
from . import views

urlpatterns = [
    #Aunthentication 
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),

    #categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/content/', views.CategoryContentView.as_view(), name='category-content'),

    #biology content
    path('content/', views.BiologyContentListView.as_view(), name='content-list'),
    path('content/<int:pk>/', views.BiologyContentDetailView.as_view(), name='content-detail'),

]