from django_filters import rest_framework

from reviews.models import Title


class TitleFilter(rest_framework.FilterSet):
    """Кастомный фильтр для произведений."""

    name = rest_framework.CharFilter(lookup_expr='iexact')
    category = rest_framework.CharFilter(field_name='category__slug')
    genre = rest_framework.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = (
            'name',
            'category',
            'genre',
            'year',
        )
