from django_filters import filterset

from core import models, choices


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
