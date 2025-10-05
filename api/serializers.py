from rest_framework import serializers
from .models import User, Category, BiologyContent

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_at']

class BiologyContentSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )
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
