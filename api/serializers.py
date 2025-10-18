from rest_framework import serializers
from .models import Category, BiologyContent
from django.contrib.auth import get_user_model

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_at']

class BiologyContentSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = BiologyContent
        fields = ['id', 'title', 'slug', 'content_body', 'summary', 'is_published', 'category', 'author', 'created_at', 'updated_at']
        def create(self, validated_data):
            return BiologyContent.objects.create(**validated_data)
        
        def update(self, instance, validated_data): 
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance

