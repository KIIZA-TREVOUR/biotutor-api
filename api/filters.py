import django_filters
from .models import BiologyContent

class BiologyContentFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    author = django_filters.NumberFilter(field_name='author', lookup_expr='exact')

    class Meta:
        model = BiologyContent
        fields = []