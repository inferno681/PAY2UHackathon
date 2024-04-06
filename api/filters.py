from django_filters.rest_framework import FilterSet, filters

from subscriptions.models import Category, Cover


class CoverFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories__name',
        to_field_name='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Cover
        fields = ('name',)
