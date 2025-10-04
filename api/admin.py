from django.contrib import admin
from .models import Category, BiologyContent

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug','created_at')
    prepopulated_fields = {'slug':('name',)}


@admin.register(BiologyContent)
class BiologyContentAdmin(admin.ModelAdmin):
    list_display = ('title','author','category','is_published','created_at')
    list_filter = ('is_published','category','author')
    search_fields = ('title','content_body')
    prepopulated_fields = {'slug':('title',)}
