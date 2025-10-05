from rest_framework import serializers
from .models import User, Category, BiologyContent

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_at']

