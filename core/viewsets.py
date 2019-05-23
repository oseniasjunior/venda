from rest_framework import viewsets
from rest_framework.decorators import action

from core import models, serializers, queries, filters


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    filter_class = filters.ZoneFilterSet

    @action(detail=False, methods=['GET'])
    def get_total_customer(self, request, *args, **kwargs):
        self.queryset = queries.total_customer_by_zone1()
        return super(ZoneViewSet, self).list(request, *args, **kwargs)


class StateViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer

    @action(detail=False, methods=['GET'])
    def get_by_name(self, request, *args, **kwargs):
        name = request.query_params['name']
        queryset = queries.get_state_by_name(name=name)
        self.queryset = queryset
        return super(StateViewSet, self).list(request, *args, **kwargs)


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = models.District.objects.select_related('city', 'zone').all()
    serializer_class = serializers.DistrictSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.select_related('state').all()
    serializer_class = serializers.CitySerializer


class StockAddressViewSet(viewsets.ModelViewSet):
    queryset = models.StockAddress.objects.all()
    serializer_class = serializers.StockAddressSerializer


class MovementStockViewSet(viewsets.ModelViewSet):
    queryset = models.MovementStock.objects.all()
    serializer_class = serializers.MovementStockSerializer
    filter_class = filters.MovementStockFilterSet


class ProductGroupViewSet(viewsets.ModelViewSet):
    queryset = models.ProductGroup.objects.all()
    serializer_class = serializers.ProductGroupSerializer
    # filter_class = filters.MovementStockFilterSet


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_class = filters.ProductFilterSet
    ordering_fields = '__all__'
    ordering = ('-id',)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer
