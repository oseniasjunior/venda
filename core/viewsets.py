from rest_framework import viewsets
from rest_framework.decorators import action

from core import models, serializers, queries


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer

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


class CityViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.select_related('state').all()
    serializer_class = serializers.CitySerializer