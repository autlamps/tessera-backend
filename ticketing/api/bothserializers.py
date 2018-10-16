from rest_framework import serializers

from ticketing.models import Route


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('id', 'name', 'description', 'cost')
