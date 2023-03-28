from django_filters import FilterSet, NumberFilter, CharFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year')
