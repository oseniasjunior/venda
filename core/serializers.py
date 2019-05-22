from rest_framework import serializers

from core import models


class SerializerBase(serializers.HyperlinkedModelSerializer):
    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.insert(0, 'id')
        return fields


class ZoneSerializer(SerializerBase):
    counter = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Zone
        fields = ['id', 'url', 'name', 'counter']


class StateSerializer(SerializerBase):
    class Meta:
        model = models.State
        fields = '__all__'


class StateLightSerializer(SerializerBase):
    class Meta:
        model = models.State
        fields = ['id', 'name']


class CitySerializer(SerializerBase):
    state_obj = StateLightSerializer(source='state', read_only=True, many=False)

    class Meta:
        model = models.City
        fields = '__all__'


class DistrictSerializer(SerializerBase):
    class Meta:
        model = models.District
        fields = '__all__'


class StockAddressSerializer(SerializerBase):
    class Meta:
        model = models.StockAddress
        fields = '__all__'


class MovementStockSerializer(SerializerBase):
    class Meta:
        model = models.MovementStock
        fields = '__all__'


class ProductGroupSerializer(SerializerBase):
    class Meta:
        model = models.ProductGroup
        fields = '__all__'


class ProductSerializer(SerializerBase):
    class Meta:
        model = models.Product
        fields = '__all__'


class SupplierSerializer(SerializerBase):
    class Meta:
        model = models.Supplier
        fields = '__all__'
