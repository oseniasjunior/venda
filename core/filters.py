from django.db.models import QuerySet, Q
from django_filters import filterset
from django_filters.widgets import BooleanWidget

from core import models, choices


class CharInFilter(filterset.BaseInFilter, filterset.CharFilter):
    pass


class ZoneFilterSet(filterset.FilterSet):
    name = filterset.CharFilter(lookup_expr=choices.LIKE)

    class Meta:
        model = models.Zone
        fields = ['name']


class DistrictFilterSet(filterset.FilterSet):
    city = filterset.CharFilter(
        lookup_expr=choices.LIKE,
        field_name='city__name'
    )
    start = filterset.DateFilter(
        lookup_expr='date__gte',
        field_name='created_at'
    )
    end = filterset.DateFilter(
        lookup_expr='date__lte',
        field_name='created_at'
    )

    class Meta:
        model = models.District
        fields = ['city']


class SaleFilterSet(filterset.FilterSet):
    year = filterset.NumberFilter(
        lookup_expr='year__exact',
        field_name='date'
    )

    class Meta:
        model = models.Sale
        fields = ['year']


class MovementStockFilterSet(filterset.FilterSet):
    type = CharInFilter(lookup_expr=choices.IN)
    active = filterset.BooleanFilter(widget=BooleanWidget)
    start = filterset.DateFilter(
        lookup_expr='gte',
        field_name='date'
    )
    end = filterset.DateFilter(
        lookup_expr='lte',
        field_name='date'
    )

    class Meta:
        model = models.MovementStock
        fields = ['type', 'active', 'start', 'end']


class ProductFilterSet(filterset.FilterSet):
    product_or_group = filterset.CharFilter(
        method='filter_product_or_group'
    )

    def filter_product_or_group(self, queryset: QuerySet, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(product_group__description__icontains=value)
        )

    class Meta:
        model = models.Product
        fields = ['product_or_group']
