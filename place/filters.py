import django_filters

from .models import Place


class PlaceFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'A-Z'),
        ('decending', 'Z-A')
    )

    sort_by = django_filters.ChoiceFilter(
        label='Sort By', choices=CHOICES, method='sort_by_title')

    class Meta:
        model = Place
        fields = {
            'title': ['icontains'],
            'city': ['icontains']
        }

    def sort_by_title(self, queryset, name, value):

        expression = 'title' if value == 'ascending' else '-title'
        return queryset.order_by(expression)
