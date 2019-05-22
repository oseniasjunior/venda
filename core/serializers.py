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
